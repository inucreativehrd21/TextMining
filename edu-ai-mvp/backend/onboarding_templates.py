# onboarding_templates.py - HRD 온보딩 교육학적 설계 템플릿 (완성판)

from typing import Dict, List, Any

# === Kirkpatrick 4단계 평가 모델 (계속) ===

KIRKPATRICK_EVALUATION_MODEL = {
    "level_1_reaction": {
        "korean": "반응 평가",
        "description": "학습자의 만족도, 참여도, 학습 경험 평가",
        "metrics": [
            "교육 만족도 (1-5점)",
            "콘텐츠 유용성 평가",
            "강사/멘토 만족도", 
            "학습 환경 평가",
            "추천 의향 (NPS)"
        ],
        "measurement_tools": ["설문조사", "피드백 폼", "실시간 반응", "포커스 그룹"],
        "target_score": 4.0,
        "collection_timing": "모듈 완료 직후"
    },
    "level_2_learning": {
        "korean": "학습 평가",
        "description": "지식 습득, 스킬 향상, 태도 변화 측정",
        "metrics": [
            "지식 습득도 (0-100점)",
            "스킬 향상도 평가",
            "태도 변화 측정",
            "자신감 증가 정도",
            "학습 목표 달성도"
        ],
        "measurement_tools": ["퀴즈", "실습 평가", "시뮬레이션", "포트폴리오", "자가 평가"],
        "target_score": 85.0,
        "collection_timing": "온보딩 중간 및 완료 시점"
    },
    "level_3_behavior": {
        "korean": "행동 평가",
        "description": "실무 적용도, 행동 변화, 성과 개선 추적",
        "metrics": [
            "업무 적용도 (1-5점)",
            "행동 변화 관찰",
            "업무 성과 개선",
            "협업 능력 향상",
            "주도성 및 참여도"
        ],
        "measurement_tools": ["360도 피드백", "행동 관찰", "성과 지표", "동료 평가", "상사 평가"],
        "target_score": 4.2,
        "collection_timing": "온보딩 완료 후 30일, 90일"
    },
    "level_4_results": {
        "korean": "결과 평가",
        "description": "조직 성과 기여도, ROI, 비즈니스 임팩트 측정",
        "metrics": [
            "업무 생산성 향상 (%)",
            "조기 이직률 감소",
            "고객 만족도 기여",
            "팀 성과 향상",
            "온보딩 ROI"
        ],
        "measurement_tools": ["성과 데이터", "이직률 통계", "고객 피드백", "재무 지표", "ROI 계산"],
        "target_score": 3.5,
        "collection_timing": "온보딩 완료 후 6개월, 1년"
    }
}

# === ADDIE 모델 기반 온보딩 설계 프레임워크 ===

ADDIE_ONBOARDING_FRAMEWORK = {
    "analyze": {
        "korean": "분석",
        "activities": [
            "조직 요구사항 분석",
            "직무 역량 분석",
            "학습자 특성 분석",
            "현재 온보딩 문제점 진단",
            "성과 차이 분석"
        ],
        "deliverables": [
            "조직 분석 리포트",
            "직무 역량 매트릭스",
            "학습자 프로필",
            "GAP 분석 결과",
            "학습 요구사항 정의"
        ],
        "tools": ["설문조사", "인터뷰", "관찰", "문서 분석", "데이터 분석"]
    },
    "design": {
        "korean": "설계",
        "activities": [
            "학습 목표 설정",
            "성과 지표 정의",
            "학습 전략 수립",
            "평가 계획 수립",
            "학습 경로 설계"
        ],
        "deliverables": [
            "학습 목표 명세서",
            "성과 지표 체계",
            "교수 설계 전략",
            "평가 계획서",
            "학습 아키텍처"
        ],
        "frameworks": ["Bloom's Taxonomy", "Gagné 9 Events", "ARCS Model", "Kirkpatrick"]
    },
    "develop": {
        "korean": "개발",
        "activities": [
            "학습 콘텐츠 제작",
            "상호작용 설계",
            "평가 도구 개발",
            "멀티미디어 제작",
            "시스템 구축"
        ],
        "deliverables": [
            "학습 모듈",
            "인터랙티브 콘텐츠",
            "평가 문항",
            "미디어 자료",
            "LMS 시스템"
        ],
        "personalization": ["학습스타일별", "성격유형별", "경험수준별", "직무별"]
    },
    "implement": {
        "korean": "실행",
        "activities": [
            "파일럿 테스트",
            "시스템 배포",
            "사용자 교육",
            "모니터링 시작",
            "지원 체계 운영"
        ],
        "deliverables": [
            "파일럿 결과 리포트",
            "배포 가이드",
            "사용자 매뉴얼",
            "모니터링 대시보드",
            "지원 프로세스"
        ],
        "success_factors": ["경영진 지원", "사용자 참여", "기술 안정성", "지속적 소통"]
    },
    "evaluate": {
        "korean": "평가",
        "activities": [
            "Kirkpatrick 4단계 평가",
            "데이터 수집 및 분석",
            "ROI 계산",
            "개선점 도출",
            "차기 버전 계획"
        ],
        "deliverables": [
            "평가 결과 리포트",
            "ROI 분석서",
            "개선 권고사항",
            "베스트 프랙티스",
            "업데이트 계획"
        ],
        "continuous_improvement": ["데이터 기반 개선", "사용자 피드백 반영", "기술 업데이트"]
    }
}

# === ARCS 동기 설계 모델 ===

ARCS_MOTIVATION_MODEL = {
    "attention": {
        "korean": "주의 집중",
        "strategies": [
            "호기심 유발",
            "감각적 자극",
            "변화와 다양성",
            "문제 제시",
            "스토리텔링"
        ],
        "onboarding_applications": [
            "CEO 웰컴 비디오",
            "성공 스토리 공유",
            "인터랙티브 퀴즈",
            "실제 업무 시뮬레이션",
            "회사 히스토리 게임"
        ],
        "techniques": ["비디오", "애니메이션", "게이미피케이션", "VR/AR", "소셜 학습"]
    },
    "relevance": {
        "korean": "관련성",
        "strategies": [
            "목표 지향성",
            "동기 부합",
            "친숙함 활용",
            "선택권 제공",
            "개인화 적용"
        ],
        "onboarding_applications": [
            "직무별 맞춤 콘텐츠",
            "개인 목표 설정",
            "이전 경험 연계",
            "학습 경로 선택",
            "멘토 매칭"
        ],
        "personalization": ["직무", "경험", "학습스타일", "성격", "관심사"]
    },
    "confidence": {
        "korean": "자신감",
        "strategies": [
            "성공 기대감 조성",
            "점진적 난이도 증가",
            "성취 경험 제공",
            "자기 효능감 강화",
            "지원 시스템 구축"
        ],
        "onboarding_applications": [
            "단계별 성취 배지",
            "마이크로 러닝",
            "진도 시각화",
            "동료 지원 네트워크",
            "멘토링 시스템"
        ],
        "confidence_builders": ["작은 성공", "피드백", "지원", "연습 기회", "안전한 환경"]
    },
    "satisfaction": {
        "korean": "만족감",
        "strategies": [
            "성취감 제공",
            "보상 시스템",
            "공정한 평가",
            "사회적 인정",
            "지속적 발전"
        ],
        "onboarding_applications": [
            "완료 인증서",
            "팀 소개 및 환영",
            "성과 인정 시스템",
            "커리어 경로 제시",
            "지속 학습 기회"
        ],
        "retention_factors": ["인정", "성장", "소속감", "기여", "의미"]
    }
}

# === 직무별 온보딩 템플릿 ===

JOB_ROLE_ONBOARDING_TEMPLATES = {
    "all_roles": {
        "common_modules": [
            {
                "title": "회사 소개 및 비전",
                "duration_hours": 2,
                "bloom_level": 2,
                "gagne_events": [1, 2],
                "content_types": ["video", "presentation", "discussion"]
            },
            {
                "title": "조직문화 및 핵심가치",
                "duration_hours": 3,
                "bloom_level": 2,
                "gagne_events": [3, 4, 5],
                "content_types": ["workshop", "case_study", "reflection"]
            },
            {
                "title": "규정 및 컴플라이언스",
                "duration_hours": 4,
                "bloom_level": 1,
                "gagne_events": [4, 7, 8],
                "content_types": ["elearning", "quiz", "certification"]
            },
            {
                "title": "커뮤니케이션 및 협업",
                "duration_hours": 3,
                "bloom_level": 3,
                "gagne_events": [5, 6, 7],
                "content_types": ["practice", "role_play", "feedback"]
            }
        ],
        "kirkpatrick_focus": ["reaction", "learning", "behavior"]
    },
    "sales": {
        "specific_modules": [
            {
                "title": "제품/서비스 완전 이해",
                "duration_hours": 8,
                "bloom_level": 3,
                "key_activities": ["제품 데모", "고객 시나리오", "경쟁사 분석"],
                "assessment": ["제품 설명 시뮬레이션", "고객 Q&A 대응"]
            },
            {
                "title": "영업 프로세스 및 CRM",
                "duration_hours": 6,
                "bloom_level": 3,
                "key_activities": ["CRM 실습", "영업 단계별 연습", "파이프라인 관리"],
                "assessment": ["CRM 활용 테스트", "영업 시나리오 실습"]
            },
            {
                "title": "고객 관계 구축",
                "duration_hours": 4,
                "bloom_level": 4,
                "key_activities": ["고객 분석", "관계 전략 수립", "커뮤니케이션 스킬"],
                "assessment": ["고객 분석 과제", "관계 구축 계획"]
            }
        ],
        "success_metrics": ["제품 지식 점수", "CRM 활용도", "첫 거래 성사율"],
        "mentoring_focus": ["실전 영업 동행", "고객 미팅 참관", "제안서 검토"]
    },
    "engineering": {
        "specific_modules": [
            {
                "title": "기술 스택 및 아키텍처",
                "duration_hours": 12,
                "bloom_level": 2,
                "key_activities": ["코드베이스 리뷰", "시스템 아키텍처 학습", "개발 환경 설정"],
                "assessment": ["환경 설정 완료", "코드 리뷰 참여"]
            },
            {
                "title": "개발 프로세스 및 협업",
                "duration_hours": 8,
                "bloom_level": 3,
                "key_activities": ["Git 워크플로우", "코드 리뷰 프로세스", "애자일 방법론"],
                "assessment": ["첫 PR 제출", "코드 리뷰 품질"]
            },
            {
                "title": "실전 프로젝트 참여",
                "duration_hours": 20,
                "bloom_level": 6,
                "key_activities": ["실제 기능 개발", "버그 수정", "문서화"],
                "assessment": ["프로젝트 기여도", "코드 품질", "문서 완성도"]
            }
        ],
        "success_metrics": ["코드 품질 점수", "PR 승인률", "프로젝트 기여도"],
        "mentoring_focus": ["코드 리뷰", "기술 멘토링", "캐리어 가이드"]
    },
    "marketing": {
        "specific_modules": [
            {
                "title": "브랜드 및 마케팅 전략",
                "duration_hours": 6,
                "bloom_level": 2,
                "key_activities": ["브랜드 가이드 학습", "마케팅 전략 이해", "타겟 고객 분석"],
                "assessment": ["브랜드 가이드 준수", "타겟 분석 과제"]
            },
            {
                "title": "마케팅 도구 및 채널",
                "duration_hours": 8,
                "bloom_level": 3,
                "key_activities": ["마케팅 툴 실습", "채널별 전략", "콘텐츠 제작"],
                "assessment": ["툴 활용 테스트", "콘텐츠 제작 과제"]
            },
            {
                "title": "캠페인 기획 및 실행",
                "duration_hours": 10,
                "bloom_level": 5,
                "key_activities": ["캠페인 기획", "예산 계획", "성과 측정"],
                "assessment": ["캠페인 기획서", "실행 계획"]
            }
        ],
        "success_metrics": ["브랜드 이해도", "툴 활용도", "캠페인 성과"],
        "mentoring_focus": ["크리에이티브 리뷰", "전략 수립", "성과 분석"]
    },
    "hr": {
        "specific_modules": [
            {
                "title": "HR 시스템 및 프로세스",
                "duration_hours": 8,
                "bloom_level": 3,
                "key_activities": ["HRIS 활용", "채용 프로세스", "평가 시스템"],
                "assessment": ["시스템 활용 테스트", "프로세스 이해도"]
            },
            {
                "title": "노동법 및 컴플라이언스",
                "duration_hours": 6,
                "bloom_level": 1,
                "key_activities": ["법규 학습", "사례 분석", "리스크 관리"],
                "assessment": ["법규 시험", "사례 분석 과제"]
            },
            {
                "title": "조직 개발 및 교육",
                "duration_hours": 8,
                "bloom_level": 4,
                "key_activities": ["교육 기획", "조직 진단", "변화 관리"],
                "assessment": ["교육 기획서", "조직 분석 리포트"]
            }
        ],
        "success_metrics": ["법규 준수율", "시스템 활용도", "교육 기획 역량"],
        "mentoring_focus": ["전문성 개발", "윤리적 판단", "전략적 사고"]
    }
}

# === 학습 스타일별 맞춤화 전략 ===

LEARNING_STYLE_STRATEGIES = {
    "visual": {
        "korean": "시각형 학습자",
        "preferences": ["이미지", "도표", "그래프", "동영상", "인포그래픽"],
        "onboarding_adaptations": [
            "조직도 시각화",
            "프로세스 플로우차트",
            "데이터 대시보드",
            "비디오 콘텐츠 중심",
            "마인드맵 활용"
        ],
        "content_formats": ["infographic", "video", "diagram", "flowchart", "dashboard"],
        "engagement_tips": ["색상 활용", "시각적 메타포", "진도 시각화", "성취 배지"]
    },
    "auditory": {
        "korean": "청각형 학습자",  
        "preferences": ["강의", "토론", "팟캐스트", "음성 설명", "그룹 활동"],
        "onboarding_adaptations": [
            "라이브 세션 증가",
            "팟캐스트 콘텐츠",
            "토론 그룹 참여",
            "음성 피드백",
            "멘토링 대화"
        ],
        "content_formats": ["podcast", "webinar", "discussion", "audio_guide", "voice_note"],
        "engagement_tips": ["음성 내비게이션", "배경음악", "발음 강조", "리듬감"]
    },
    "reading": {
        "korean": "읽기/쓰기형 학습자",
        "preferences": ["텍스트", "문서", "노트", "체크리스트", "글쓰기"],
        "onboarding_adaptations": [
            "상세 매뉴얼 제공",
            "체크리스트 활용",
            "노트 템플릿",
            "글쓰기 과제",
            "문서 중심 학습"
        ],
        "content_formats": ["manual", "checklist", "worksheet", "article", "template"],
        "engagement_tips": ["구조화된 텍스트", "키워드 강조", "요약본", "글로서리"]
    },
    "kinesthetic": {
        "korean": "체감형 학습자",
        "preferences": ["실습", "시뮬레이션", "체험", "움직임", "조작"],
        "onboarding_adaptations": [
            "핸즈온 워크샵",
            "시뮬레이션 증가",
            "실제 업무 체험",
            "인터랙티브 활동",
            "프로젝트 기반 학습"
        ],
        "content_formats": ["simulation", "workshop", "lab", "game", "project"],
        "engagement_tips": ["터치 인터페이스", "드래그 앤 드롭", "게이미피케이션", "실습 중심"]
    }
}

# === 성격 유형별 온보딩 전략 (MBTI 기반 간소화) ===

PERSONALITY_TYPE_STRATEGIES = {
    "analyst": {
        "korean": "분석가형 (NT)",
        "characteristics": ["논리적", "체계적", "혁신적", "독립적", "이론 선호"],
        "onboarding_approach": [
            "논리적 구조 제시",
            "시스템 전체 그림",
            "혁신 기회 강조",
            "자율성 보장",
            "깊이 있는 학습"
        ],
        "content_preferences": ["framework", "system_design", "theory", "analysis", "research"],
        "motivation_factors": ["지적 도전", "시스템 이해", "혁신 기회", "전문성 개발"]
    },
    "diplomat": {
        "korean": "외교관형 (NF)", 
        "characteristics": ["인간 중심", "가치 지향", "창의적", "협력적", "성장 지향"],
        "onboarding_approach": [
            "가치와 의미 강조",
            "인간관계 중심",
            "성장 기회 제시",
            "협력 활동 증가",
            "개인적 연결"
        ],
        "content_preferences": ["story", "values", "people", "growth", "collaboration"],
        "motivation_factors": ["의미있는 일", "인간관계", "개인 성장", "기여 가치"]
    },
    "sentinel": {
        "korean": "관리자형 (SJ)",
        "characteristics": ["안정성 중시", "절차 선호", "책임감", "현실적", "단계적"],
        "onboarding_approach": [
            "명확한 절차 제시",
            "단계별 진행",
            "안정감 제공",
            "책임 영역 명확화",
            "전통과 규칙 강조"
        ],
        "content_preferences": ["procedure", "checklist", "step_by_step", "rules", "structure"],
        "motivation_factors": ["안정성", "명확성", "인정", "소속감", "기여도"]
    },
    "explorer": {
        "korean": "탐험가형 (SP)",
        "characteristics": ["유연성", "현재 중심", "실용적", "적응적", "경험 선호"],
        "onboarding_approach": [
            "실용적 내용 중심",
            "유연한 학습 경로",
            "즉시 적용 가능",
            "다양한 경험 제공",
            "재미 요소 추가"
        ],
        "content_preferences": ["practical", "flexible", "variety", "experience", "fun"],
        "motivation_factors": ["실용성", "자유도", "재미", "즉시 보상", "다양성"]
    }
}

# === 온보딩 성공 지표 체계 ===

ONBOARDING_SUCCESS_METRICS = {
    "engagement_metrics": {
        "completion_rate": {"target": 95, "unit": "%", "measurement": "weekly"},
        "time_to_complete": {"target": 28, "unit": "days", "measurement": "individual"},
        "login_frequency": {"target": 5, "unit": "times/week", "measurement": "weekly"},
        "content_interaction": {"target": 80, "unit": "%", "measurement": "module"}
    },
    "learning_metrics": {
        "knowledge_retention": {"target": 85, "unit": "%", "measurement": "post_test"},
        "skill_demonstration": {"target": 4.0, "unit": "1-5 scale", "measurement": "assessment"},
        "confidence_level": {"target": 4.2, "unit": "1-5 scale", "measurement": "survey"}
    },
    "performance_metrics": {
        "productivity_ramp": {"target": 75, "unit": "% of full productivity", "measurement": "30_days"},
        "quality_score": {"target": 4.0, "unit": "1-5 scale", "measurement": "supervisor_rating"},
        "integration_speed": {"target": 21, "unit": "days to full integration", "measurement": "milestone"}
    },
    "retention_metrics": {
        "30_day_retention": {"target": 98, "unit": "%", "measurement": "monthly"},
        "90_day_retention": {"target": 95, "unit": "%", "measurement": "quarterly"},
        "1_year_retention": {"target": 85, "unit": "%", "measurement": "annual"},
        "satisfaction_score": {"target": 4.3, "unit": "1-5 scale", "measurement": "survey"}
    },
    "business_metrics": {
        "time_to_productivity": {"target": 30, "unit": "days", "measurement": "milestone"},
        "onboarding_cost_per_hire": {"target": 2000, "unit": "USD", "measurement": "total"},
        "roi_calculation": {"target": 3.5, "unit": "ratio", "measurement": "annual"},
        "manager_satisfaction": {"target": 4.2, "unit": "1-5 scale", "measurement": "survey"}
    }
}

# === 산업별 맞춤화 전략 ===

INDUSTRY_CUSTOMIZATION = {
    "it_software": {
        "culture_focus": ["혁신", "애자일", "기술 우선", "빠른 변화"],
        "key_challenges": ["기술 격차", "빠른 변화", "원격 협업", "번아웃"],
        "onboarding_priorities": ["기술 스택", "개발 프로세스", "협업 도구", "지속적 학습"]
    },
    "finance": {
        "culture_focus": ["정확성", "컴플라이언스", "신뢰", "리스크 관리"],
        "key_challenges": ["규제 준수", "보안", "정확성", "압박감"],
        "onboarding_priorities": ["법규", "시스템", "절차", "윤리"]
    },
    "manufacturing": {
        "culture_focus": ["품질", "안전", "효율성", "표준화"],
        "key_challenges": ["안전", "품질 관리", "효율성", "기술 변화"],
        "onboarding_priorities": ["안전 교육", "품질 시스템", "생산 프로세스", "개선 활동"]
    },
    "retail": {
        "culture_focus": ["고객 서비스", "판매", "브랜드", "시즌성"],
        "key_challenges": ["고객 대응", "재고 관리", "시즌 변동", "직원 순환"],
        "onboarding_priorities": ["고객 서비스", "제품 지식", "시스템", "브랜드"]
    }
}
