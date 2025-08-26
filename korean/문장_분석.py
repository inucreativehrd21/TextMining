
# -*- coding: utf-8 -*-
"""
Okt 기반 형태소 분석 + 한글 초/중/종성 분해
- 외부 API 없음. KoNLPy(Okt)만 사용.
- CoT 로그 옵션 지원(cot=True)
- Self-Consistency: stem/norm 옵션 조합 비교로 간단한 일관성 점검

설정 팁:
- filter_pos로 세고 싶은 품사만 고르면 됨 (예: ["Noun","Verb","Adjective","Adverb","Josa","Eomi"])
"""

import re
from collections import Counter
from typing import Dict, Tuple, List, Optional

from konlpy.tag import Okt
okt = Okt()

HANGUL_BASE = 0xAC00
CHOSUNG_LIST = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
JUNGSUNG_LIST = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]
JONGSUNG_LIST = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

def decompose_hangul(text: str, cot_log: Optional[List[str]] = None) -> Tuple[Counter, Counter, Counter]:
    cho_c, jung_c, jong_c = Counter(), Counter(), Counter()
    for ch in text or "":
        code = ord(ch)
        if 0xAC00 <= code <= 0xD7A3:
            syl = code - HANGUL_BASE
            cho_idx = syl // (21 * 28)
            jung_idx = (syl % (21 * 28)) // 28
            jong_idx = syl % 28
            cho_c[CHOSUNG_LIST[cho_idx]] += 1
            jung_c[JUNGSUNG_LIST[jung_idx]] += 1
            if jong_idx != 0:
                jong_c[JONGSUNG_LIST[jong_idx]] += 1
    if cot_log is not None:
        cot_log.append(f"[자모 합계] 초성:{sum(cho_c.values())}, 중성:{sum(jung_c.values())}, 종성:{sum(jong_c.values())}")
    return cho_c, jung_c, jong_c

def okt_morph_count(
    text: str,
    *,
    norm: bool = True,
    stem: bool = True,
    filter_pos: Optional[List[str]] = None,
    lowercase_non_korean: bool = True,
    cot_log: Optional[List[str]] = None
) -> Tuple[Counter, Counter]:
    """
    Okt로 형태소 분석 후 빈도 카운트.
    - filter_pos 지정 시 해당 품사만 카운트 (None이면 모든 품사 포함)
    - non-Korean 토큰은 소문자 변환 옵션 제공
    반환: (morph_counter, pos_counter)
    """
    pos = okt.pos(text or "", norm=norm, stem=stem)
    if cot_log is not None:
        cot_log.append(f"[Okt.pos] norm={norm}, stem={stem} -> 샘플: {pos[:10]}")

    morphs = []
    pos_counter = Counter(tag for _, tag in pos)
    for surface, tag in pos:
        keep = (filter_pos is None) or (tag in filter_pos)
        if not keep:
            continue
        tok = surface
        # 비한글(영문/숫자 등)은 옵션에 따라 소문자화
        if lowercase_non_korean and not re.fullmatch(r"[가-힣]+", tok):
            tok = tok.lower()
            if cot_log is not None and tok != surface:
                cot_log.append(f"[비한글 소문자화] {surface} -> {tok}")
        morphs.append(tok)

    cnt = Counter(morphs)
    if cot_log is not None:
        cot_log.append(f"[형태소 카운트] top5 -> {cnt.most_common(5)}")
        cot_log.append(f"[품사 분포] top5 -> {pos_counter.most_common(5)}")
    return cnt, pos_counter

def analyze_okt(
    text: str,
    *,
    cot: bool = False,
    filter_pos: Optional[List[str]] = None,
    self_consistency: bool = True
) -> Dict:
    """
    Okt 기반 최종 분석.
    - filter_pos: 세고 싶은 품사만 지정 (예: ["Noun","Verb","Adjective","Adverb","Josa","Eomi"])
    - self_consistency: (norm,stem) 조합을 바꿔 한 번 더 세어 결과 차이를 비교
    """
    cot_log: Optional[List[str]] = [] if cot else None
    if cot_log is not None:
        cot_log.append("[시작] Okt 분석 시작")

    # 1) 기본 설정으로 형태소 카운트
    morph, pos_dist = okt_morph_count(
        text,
        norm=True, stem=True,
        filter_pos=filter_pos,
        lowercase_non_korean=True,
        cot_log=cot_log
    )

    # 2) Self-Consistency: 다른 설정으로 다시 세서 비교 (예: norm=False, stem=False)
    sc_note = None
    if self_consistency:
        alt_morph, _ = okt_morph_count(
            text,
            norm=False, stem=False,
            filter_pos=filter_pos,
            lowercase_non_korean=True,
            cot_log=None
        )
        if morph != alt_morph:
            diff_keys = set(morph.keys()) ^ set(alt_morph.keys())
            sc_note = {
                "diff_keys_count": len(diff_keys),
                "example_diffs": (
                    list((morph - alt_morph).most_common(3)) +
                    list((alt_morph - morph).most_common(3))
                )
            }
            if cot_log is not None:
                cot_log.append(f"[Self-Consistency] 설정 변경에 따라 형태소 분포 차이 발견. 변경 키 수: {len(diff_keys)}")
        else:
            if cot_log is not None:
                cot_log.append("[Self-Consistency] 대체 설정과 동일 결과")

    # 3) 한글 자모 분해
    cho, jung, jong = decompose_hangul(text, cot_log)

    # 4) 요약
    result = {
        "morph_top10": morph.most_common(10),
        "pos_top10": pos_dist.most_common(10),
        "chosung_top10": cho.most_common(10),
        "jungsung_top10": jung.most_common(10),
        "jongsung_top10": jong.most_common(10),
        "totals": {
            "초성_합계": sum(cho.values()),
            "중성_합계": sum(jung.values()),
            "종성_합계": sum(jong.values()),
        }
    }
    if sc_note is not None:
        result["self_consistency"] = sc_note
    if cot_log is not None:
        cot_log.append("[완료] 분석 종료")
        result["cot_log"] = cot_log
    return result

def pretty_print(result: Dict, show_cot: bool = False) -> None:
    print("[형태소 상위 10]")
    for k, v in result["morph_top10"]:
        print(f"- {k}: {v}")
    print("\n[품사 상위 10]")
    for k, v in result["pos_top10"]:
        print(f"- {k}: {v}")
    print("\n[초성 상위 10]")
    for k, v in result["chosung_top10"]:
        print(f"- {k}: {v}")
    print("\n[중성 상위 10]")
    for k, v in result["jungsung_top10"]:
        print(f"- {k}: {v}")
    print("\n[종성 상위 10]")
    for k, v in result["jongsung_top10"]:
        print(f"- {k}: {v}")
    print("\n[합계]")
    for k, v in result["totals"].items():
        print(f"- {k}: {v}")
    if "self_consistency" in result:
        sc = result["self_consistency"]
        print("\n[Self-Consistency 체크]")
        print(f"- 변경 키 수: {sc['diff_keys_count']}")
        print(f"- 차이 예시: {sc['example_diffs'][:5]}")
    if show_cot and "cot_log" in result:
        print("\n[CoT 로그]")
        for line in result["cot_log"]:
            print(line)

if __name__ == "__main__":
    sample_texts = [
        "오늘은 서울에서 비가 조금 내렸고, 바람이 선선했다.",
        "AI 기술이 빠르게 발전하고 있다.",
        "나는 어제 친구와 영화를 봤다.",
        "점심으로 비빔밥을 먹고 싶다.",
        "프로젝트 마감일이 다가오고 있다.",
        "코딩은 재미있지만 가끔은 어렵다.",
        "한국의 전통 음식에는 김치가 있다.",
        "오늘 날씨가 매우 덥다.",
        "강아지가 공원에서 뛰어놀고 있다.",
        "책을 읽는 것은 좋은 습관이다.",
        "바다에서 수영하는 것을 좋아한다.",
        "학교에 가는 길에 비가 내렸다.",
        "커피 한 잔이 필요하다.",
        "저녁에 운동을 하러 갈 계획이다.",
        "영화관에서 새로운 영화를 개봉했다.",
        "컴퓨터 프로그래밍을 배우고 있다.",
        "음악을 들으며 산책하는 것이 즐겁다.",
        "시험 준비를 위해 열심히 공부했다.",
        "여행을 가기 전에 짐을 싸야 한다.",
        "새로운 언어를 배우는 것은 도전이다."
    ]

    for i, text in enumerate(sample_texts, start=1):
        print(f"\n=== 예시 {i} ===")
        print("입력 문장:", text)
        res = analyze_okt(text, cot=False, filter_pos=None, self_consistency=False)
        pretty_print(res, show_cot=False)
