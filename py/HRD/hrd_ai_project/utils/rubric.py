
from typing import Dict
from schema import Artifact

def score_gagne(events: Dict) -> float:
    req = ["gain_attention","inform_learners_of_objectives","stimulate_recall",
           "present_stimulus","provide_learning_guidance","elicit_performance",
           "provide_feedback","assess_performance","enhance_retention_transfer"]
    hits = sum(1 for k in req if events.get(k))
    return hits/len(req)

def score_alignment(artifact: Artifact) -> float:
    # 단순 키워드 매칭(시작점): outcome 동사 ↔ activities/assessment 텍스트
    verbs = {o.bloom.lower() for o in artifact.program.outcomes}
    text = " ".join([a.get("type","")+" "+a.get("desc","") for m in artifact.program.modules for a in m.activities])
    text += " ".join([a.get("type","")+" "+a.get("desc","") for m in artifact.program.modules for a in m.assessment])
    hit = sum(1 for v in verbs if v in text.lower())
    return min(1.0, hit / max(1, len(verbs)))

def score_transfer(artifact: Artifact) -> float:
    # 전이 트리거(상사승인/알림/코칭/현업과제) 키워드 탐지
    keys = ["상사", "알림", "코칭", "현업", "전이"]
    txt = str(artifact.model_dump())
    hit = sum(1 for k in keys if k in txt)
    return min(1.0, hit/4)

def score_kpi_link(artifact: Artifact) -> float:
    return 1.0 if all(o.kpi_link for o in artifact.program.outcomes) else 0.5

def score_accessibility(artifact: Artifact) -> float:
    return 1.0 if artifact.accessibility.get("udl_check") else 0.0

def score_operations(artifact: Artifact) -> float:
    dur_ok = 1.0 if 1 <= artifact.program.duration_hours <= 24 else 0.5
    return dur_ok

def auto_score(artifact: Artifact) -> float:
    # 가중치: 정렬(0.25), Gagne(0.2), 전이(0.2), KPI(0.15), UX/접근(0.1), 운영(0.1)
    m = artifact.program.modules[0].events_of_instruction.model_dump()
    s = (0.25*score_alignment(artifact) + 0.2*score_gagne(m) +
         0.2*score_transfer(artifact) + 0.15*score_kpi_link(artifact) +
         0.1*score_accessibility(artifact) + 0.1*score_operations(artifact))
    return round(s, 3)
