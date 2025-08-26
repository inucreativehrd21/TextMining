
import json
from dotenv import load_dotenv
from agents import domain_planner, ids_designer, lxd_ideation, meta_critic
from schema import Artifact
from rubric import auto_score

load_dotenv()

# 1) 파일럿 스펙(예시: HRD 중간 레벨, 전이 설계)
spec = {
  "domain":"HRD","level":"중간","audience_size":30,"delivery":"혼합",
  "duration_hours":8,"budget_tier":"M",
  "constraints":["법정준수","접근성(UDL)","현업시간 10% 이내"],
  "business_kpi":["L3: 코칭 주1회","L4: NPS +3pt"]
}

# 2) 라운드 실행
ctx = domain_planner(spec)
draft_json = ids_designer(ctx)
ideas = lxd_ideation(draft_json)
revised_json = meta_critic(draft_json, ideas)

# 3) 스키마 검증 & 자동 점수
artifact = Artifact.model_validate_json(revised_json)
score = auto_score(artifact)
artifact.scores.update({"auto_rubric": score, "final": score})

# 4) 저장
out = json.dumps(artifact.model_dump(), ensure_ascii=False, indent=2)
open("artifact_round1.json","w", encoding="utf-8").write(out)
print(f"[AUTO SCORE] {score}\nartifact_round1.json 생성 완료")
