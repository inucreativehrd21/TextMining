
from typing import List
from providers import OpenAIClient, PerplexityClient, GeminiClient, Msg
from schema import Artifact
import json

# 역할→모델 매핑 (초기 권장)
# - 도메인 리서치/시장 레퍼런스: Perplexity (웹기반 Q/A 강점) :contentReference[oaicite:5]{index=5}
# - 교수설계 구조화(스키마/JSON): OpenAI (JSON/함수호출 안정적) :contentReference[oaicite:6]{index=6}
# - 학습경험/아이데이션: Gemini (속도·멀티모달 프롬프트 확장 용이) :contentReference[oaicite:7]{index=7}

px = PerplexityClient(model="sonar-pro")
oa = OpenAIClient(model="gpt5")
gm = GeminiClient(model="gemini-2.0-flash")

def domain_planner(spec: dict) -> str:
    sys = "너는 HRD 전략 기획자다. L3/L4 연결 성과가설지도를 먼저 만든다."
    usr = f"조직상황/제약/대상/목표:\n{json.dumps(spec, ensure_ascii=False, indent=2)}\n" \
          f"- 전이 방해요인과 완화전략을 목록화하라."
    r = px.chat([Msg(role="system", content=sys), Msg(role="user", content=usr)], temperature=0.2)
    return r.text

def ids_designer(context_text: str) -> str:
    sys = "너는 교수설계자(ID). JSON 스키마를 반드시 준수하여 산출물을 생성한다."
    usr = f"""다음 컨텍스트를 반영해 HRD 프로그램 초안을 JSON으로 작성:
- 가네 9사태 매핑을 포함
- 목표-활동-평가 정렬
- 전이 트리거(상사/알림/코칭/현업과제) 포함
컨텍스트:
{context_text}

다음 형식으로만 출력(JSON):
{{
  "meta": {{"domain":"HRD","level":"중간","round":1,"version":1}},
  "program": {{
    "goals": [...],
    "outcomes": [{{"statement":"...","bloom":"Apply","kpi_link":"..."}}, ...],
    "modules": [
      {{
        "title":"...",
        "events_of_instruction": {{
          "gain_attention":"...", "inform_learners_of_objectives":"...",
          "stimulate_recall":"...", "present_stimulus":"...",
          "provide_learning_guidance":"...", "elicit_performance":"...",
          "provide_feedback":"...", "assess_performance":"...",
          "enhance_retention_transfer":"..."
        }},
        "activities":[{{"type":"...","desc":"...","time_min":30}}],
        "assessment":[{{"type":"...","desc":"...","rubric_id":"R1"}}]
      }}
    ],
    "delivery":"혼합","duration_hours":8
  }},
  "operations": {{"resources":["사내강사"],"budget_tier":"M","schedule":"2주"}},
  "compliance": {{"legal_training": false, "privacy":"가명화"}},
  "accessibility": {{"udl_check": true}},
  "feedback": [],
  "scores": {{"auto_rubric": null, "human_weighted": null, "final": null}}
}}"""
    r = oa.chat(
        [Msg(role="system", content=sys), Msg(role="user", content=usr)],
        response_format={"type":"json_object"}, temperature=0.1
    )
    return r.text  # JSON string

def lxd_ideation(artifact_json: str) -> str:
    sys = "너는 학습경험 디자이너. 활동과 피드백을 더 몰입감 있게 개선한다."
    usr = f"현재 산출물(JSON):\n{artifact_json}\n개선 아이디어 5가지를 불릿으로."
    r = gm.chat([Msg(role="system", content=sys), Msg(role="user", content=usr)], temperature=0.5)
    return r.text

def meta_critic(artifact_json: str, comments: str) -> str:
    sys = "너는 메타-크리틱. 아이디어를 반영하되 스키마를 지켜 JSON만 출력."
    usr = f"원본 JSON:\n{artifact_json}\n개선 포인트:\n{comments}\n=> 수정된 JSON만 출력."
    r = oa.chat([Msg(role="system", content=sys), Msg(role="user", content=usr)],
                response_format={"type":"json_object"}, temperature=0.2)
    return r.text
