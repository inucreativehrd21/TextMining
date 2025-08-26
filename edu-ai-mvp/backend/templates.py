# templates.py - HRD 온보딩 전체 템플릿 시스템 (완전 리팩토링)

from typing import Dict, List, Any

# === 기존 Git 템플릿을 HRD 온보딩으로 완전 대체 ===

# === 조직 문화별 온보딩 접근법 ===
ORGANIZATIONAL_CULTURE_TEMPLATES = {
    "hierarchical": {
        "korean": "위계형 조직",
        "onboarding_approach": {
            "emphasis": ["명확한 보고 체계", "권한과 책임", "절차 준수", "규정 숙지"],
            "learning_style": "structured",
            "pace": "systematic",
            "communication": "formal",
            "mentoring": "senior_guided"
        },
        "key_modules": [
            {"title": "조직 구조 및 보고 체계", "priority": "high", "duration_hours": 3},
            {"title": "권한과 책임 이해", "priority": "high", "duration_hours": 2},
            {"title": "업무 절차 및 프로세스", "priority": "high", "duration_hours": 4},
            {"title": "규정 및 정책 숙지", "priority": "medium", "duration_hours": 3}
        ],
        "success_factors": ["절차 준수", "명확한 소통", "단계적 성장"],
        "risk_factors": ["경직성", "창의성 부족", "의사소통 장벽"]
    },
    "collaborative": {
        "korean": "협업형 조직", 
        "onboarding_approach": {
            "emphasis": ["팀워크", "소통 스킬", "상호 협력", "네트워킹"],
            "learning_style": "interactive",
            "pace": "flexible",
            "communication": "open",
            "mentoring": "peer_supported"
        },
        "key_modules": [
            {"title": "팀워크 및 협업 스킬", "priority": "high", "duration_hours": 4},
            {"title": "효과적 커뮤니케이션", "priority": "high", "duration_hours": 3},
            {"title": "네트워킹 및 관계 구축", "priority": "high", "duration_hours": 2},
            {"title": "갈등 해결 및 조정", "priority": "medium", "duration_hours": 2}
        ],
        "success_factors": ["관계 형성", "소통 능력", "협업 성과"],
        "risk_factors": ["의견 충돌", "결정 지연", "책임 분산"]
    },
    "innovative": {
        "korean": "혁신형 조직",
        "onboarding_approach": {
            "emphasis": ["창의성", "변화 수용", "실험 정신", "지속 학습"],
            "learning_style": "experimental", 
            "pace": "adaptive",
            "communication": "creative",
            "mentoring": "innovation_focused"
        },
        "key_modules": [
            {"title": "혁신 사고 및 창의성", "priority": "high", "duration_hours": 3},
            {"title": "변화 관리 및 적응", "priority": "high", "duration_hours": 3},
            {"title": "실험 및 프로토타이핑", "priority": "medium", "duration_hours": 4},
            {"title": "지속적 학습 문화", "priority": "high", "duration_hours": 2}
        ],
        "success_factors": ["창의적 사고", "빠른 적응", "학습 의욕"],
        "risk_factors": ["불확실성", "과도한 실험", "일관성 부족"]
    },
    "results_oriented": {
        "korean": "성과중심형 조직",
        "onboarding_approach": {
            "emphasis": ["목표 설정", "성과 측정", "효율성", "경쟁력"],
            "learning_style": "goal_oriented",
            "pace": "intensive", 
            "communication": "direct",
            "mentoring": "performance_focused"
        },
        "key_modules": [
            {"title": "목표 설정 및 관리", "priority": "high", "duration_hours": 3},
            {"title": "성과 측정 및 평가", "priority": "high", "duration_hours": 3},
            {"title": "효율성 및 생산성 향상", "priority": "high", "duration_hours": 3},
            {"title": "경쟁력 강화 전략", "priority": "medium", "duration_hours": 2}
        ],
        "success_factors": ["목표 달성", "효율성", "성과 창출"],
        "risk_factors": ["과도한 압박", "번아웃", "단기 집중"]
    }
}

# === 산업별 특화 온보딩 템플릿 ===
INDUSTRY_SPECIFIC_TEMPLATES = {
    "it_software": {
        "korean": "IT/소프트웨어",
        "industry_characteristics": {
            "pace": "fast",
            "change_frequency": "high", 
            "learning_intensity": "continuous",
            "collaboration_style": "agile"
        },
        "critical_onboarding_areas": [
            "기술 스택 이해",
            "개발 프로세스 및 방법론", 
            "코드 품질 및 리뷰",
            "보안 및 컴플라이언스",
            "애자일/스크럼 문화"
        ],
        "specialized_modules": [
            {
                "title": "개발 환경 및 도구 설정",
                "duration_hours": 8,
                "bloom_level": 3,
                "mandatory": True,
                "content": ["IDE 설정", "Git 워크플로우", "CI/CD 파이프라인", "개발 서버 접근"]
            },
            {
                "title": "코드 품질 및 리뷰 프로세스", 
                "duration_hours": 6,
                "bloom_level": 4,
                "mandatory": True,
                "content": ["코딩 표준", "리뷰 프로세스", "정적 분석", "테스트 커버리지"]
            },
            {
                "title": "애자일 개발 문화",
                "duration_hours": 4,
                "bloom_level": 2,
                "mandatory": True, 
                "content": ["스크럼 이해", "스프린트 참여", "데일리 스탠드업", "회고 문화"]
            }
        ],
        "success_metrics": [
            "첫 PR 제출 시간",
            "코드 리뷰 통과율", 
            "스프린트 참여도",
            "기술 스택 이해도"
        ]
    },
    "finance": {
        "korean": "금융",
        "industry_characteristics": {
            "pace": "measured",
            "change_frequency": "low",
            "learning_intensity": "thorough",
            "collaboration_style": "formal"
        },
        "critical_onboarding_areas": [
            "금융 규제 및 컴플라이언스",
            "리스크 관리",
            "고객 정보 보안",
            "정확성 및 품질 관리",
            "윤리 및 청렴성"
        ],
        "specialized_modules": [
            {
                "title": "금융 규제 및 법규",
                "duration_hours": 12,
                "bloom_level": 1,
                "mandatory": True,
                "content": ["바젤 규제", "자본건전성", "소비자보호", "개인정보보호"]
            },
            {
                "title": "리스크 관리 체계",
                "duration_hours": 8,
                "bloom_level": 2,
                "mandatory": True,
                "content": ["신용리스크", "시장리스크", "운영리스크", "유동성리스크"]
            },
            {
                "title": "윤리 및 청렴성",
                "duration_hours": 4,
                "bloom_level": 1,
                "mandatory": True,
                "content": ["윤리강령", "이해충돌", "내부신고", "부패방지"]
            }
        ],
        "success_metrics": [
            "규제 이해도 테스트 점수",
            "컴플라이언스 준수율",
            "리스크 인식 정도",
            "윤리 교육 완료율"
        ]
    },
    "manufacturing": {
        "korean": "제조업",
        "industry_characteristics": {
            "pace": "steady",
            "change_frequency": "medium",
            "learning_intensity": "practical",
            "collaboration_style": "structured"
        },
        "critical_onboarding_areas": [
            "안전 규정 및 절차",
            "품질 관리 시스템",
            "생산 프로세스",
            "설비 운영",
            "지속적 개선 활동"
        ],
        "specialized_modules": [
            {
                "title": "산업 안전 및 보건",
                "duration_hours": 16,
                "bloom_level": 1,
                "mandatory": True,
                "content": ["안전 규정", "위험물 취급", "응급처치", "사고 예방"]
            },
            {
                "title": "품질 관리 시스템",
                "duration_hours": 12,
                "bloom_level": 2, 
                "mandatory": True,
                "content": ["ISO 9001", "품질 표준", "검사 절차", "불량 처리"]
            },
            {
                "title": "린 매뉴팩처링",
                "duration_hours": 8,
                "bloom_level": 3,
                "mandatory": False,
                "content": ["5S 활동", "카이젠", "JIT", "낭비 제거"]
            }
        ],
        "success_metrics": [
            "안전 교육 이수율",
            "품질 시험 점수",
            "생산 프로세스 이해도",
            "개선 제안 건수"
        ]
    },
    "retail": {
        "korean": "소매업",
        "industry_characteristics": {
            "pace": "variable",
            "change_frequency": "high",
            "learning_intensity": "customer_focused", 
            "collaboration_style": "service_oriented"
        },
        "critical_onboarding_areas": [
            "고객 서비스 스킬",
            "제품 지식",
            "판매 기법",
            "재고 관리",
            "브랜드 가치"
        ],
        "specialized_modules": [
            {
                "title": "고객 서비스 우수성",
                "duration_hours": 10,
                "bloom_level": 3,
                "mandatory": True,
                "content": ["서비스 마인드", "고객 응대", "불만 처리", "고객 만족"]
            },
            {
                "title": "제품 지식 및 영업",
                "duration_hours": 12,
                "bloom_level": 2,
                "mandatory": True,
                "content": ["제품 특성", "경쟁사 비교", "판매 기법", "상황별 추천"]
            },
            {
                "title": "매장 운영 및 관리",
                "duration_hours": 8,
                "bloom_level": 3,
                "mandatory": True,
                "content": ["재고 관리", "진열 기법", "POS 시스템", "매출 분석"]
            }
        ],
        "success_metrics": [
            "고객 만족도 점수",
            "제품 지식 테스트",
            "판매 실적",
            "서비스 품질 평가"
        ]
    }
}

# === 직급별 온보딩 강도 조정 템플릿 ===
JOB_LEVEL_ADJUSTMENT_TEMPLATES = {
    "entry": {
        "korean": "신입급",
        "characteristics": ["기초 부족", "높은 학습 의욕", "체계적 교육 필요", "멘토링 의존"],
        "onboarding_adjustments": {
            "duration_multiplier": 1.5,
            "detail_level": "comprehensive",
            "support_intensity": "high",
            "practice_opportunities": "extensive"
        },
        "focus_areas": [
            "기초 개념 및 원리",
            "회사 시스템 숙지",
            "기본 업무 스킬",
            "조직 적응",
            "멘토 관계 구축"
        ],
        "learning_approach": {
            "structure": "highly_structured",
            "feedback_frequency": "daily",
            "checkpoint_interval": "weekly",
            "mentoring_ratio": "1:1"
        }
    },
    "junior": {
        "korean": "주니어급",
        "characteristics": ["기본 경험 보유", "빠른 학습", "실무 적용 집중", "자율성 증가"],
        "onboarding_adjustments": {
            "duration_multiplier": 1.2,
            "detail_level": "focused",
            "support_intensity": "medium",
            "practice_opportunities": "targeted"
        },
        "focus_areas": [
            "회사별 특화 지식",
            "고급 업무 스킬",
            "팀 협업",
            "프로젝트 참여",
            "전문성 개발"
        ],
        "learning_approach": {
            "structure": "semi_structured", 
            "feedback_frequency": "bi_daily",
            "checkpoint_interval": "bi_weekly",
            "mentoring_ratio": "1:2"
        }
    },
    "mid": {
        "korean": "중급",
        "characteristics": ["풍부한 경험", "자기 주도 학습", "리더십 개발", "전략적 사고"],
        "onboarding_adjustments": {
            "duration_multiplier": 1.0,
            "detail_level": "strategic",
            "support_intensity": "low",
            "practice_opportunities": "leadership_focused"
        },
        "focus_areas": [
            "조직 전략 이해",
            "리더십 스킬",
            "크로스 펑셔널 협업",
            "혁신 및 개선",
            "후배 멘토링"
        ],
        "learning_approach": {
            "structure": "flexible",
            "feedback_frequency": "weekly", 
            "checkpoint_interval": "monthly",
            "mentoring_ratio": "1:3"
        }
    },
    "senior": {
        "korean": "시니어급",
        "characteristics": ["전문가급 지식", "전략적 역할", "변화 주도", "조직 기여"],
        "onboarding_adjustments": {
            "duration_multiplier": 0.8,
            "detail_level": "executive",
            "support_intensity": "minimal",
            "practice_opportunities": "strategic_impact"
        },
        "focus_areas": [
            "조직 비전 및 전략",
            "경영진 네트워킹",
            "변화 리더십",
            "문화 조성",
            "성과 창출"
        ],
        "learning_approach": {
            "structure": "self_directed",
            "feedback_frequency": "on_demand",
            "checkpoint_interval": "quarterly", 
            "mentoring_ratio": "reverse_mentoring"
        }
    }
}

# === 통합 온보딩 템플릿 시스템 ===
COMPREHENSIVE_ONBOARDING_TEMPLATES = {
    "templates": {
        "organizational_culture": ORGANIZATIONAL_CULTURE_TEMPLATES,
        "industry_specific": INDUSTRY_SPECIFIC_TEMPLATES,
        "job_level_adjustments": JOB_LEVEL_ADJUSTMENT_TEMPLATES
    },
    "template_selection_criteria": {
        "primary": "job_role",
        "secondary": "organizational_culture", 
        "tertiary": "industry_type",
        "adjustments": ["job_level", "experience_years", "learning_style", "personality_type"]
    },
    "template_combination_rules": {
        "base_template": "industry_specific + job_role",
        "cultural_overlay": "organizational_culture",
        "level_adjustment": "job_level_adjustments",
        "personalization": "individual_characteristics"
    }
}

# === 온보딩 성공 패턴 템플릿 ===
SUCCESS_PATTERN_TEMPLATES = {
    "high_performers": {
        "characteristics": [
            "빠른 적응력",
            "적극적 학습 태도", 
            "네트워킹 능력",
            "피드백 수용성",
            "목표 지향성"
        ],
        "common_onboarding_elements": [
            "도전적 과제 부여",
            "빠른 실무 투입",
            "다양한 경험 기회",
            "네트워킹 지원",
            "커리어 로드맵 제시"
        ],
        "success_indicators": [
            "30일 내 독립 업무 수행",
            "동료/상사 높은 평가",
            "자발적 학습 활동",
            "개선 아이디어 제시",
            "팀 기여도 우수"
        ]
    },
    "steady_performers": {
        "characteristics": [
            "체계적 학습 선호",
            "안정적 성장",
            "협력적 성향",
            "규칙 준수",
            "꾸준한 노력"
        ],
        "common_onboarding_elements": [
            "구조화된 학습 과정",
            "단계적 책임 증가",
            "충분한 연습 기회", 
            "정기적 피드백",
            "명확한 기대치"
        ],
        "success_indicators": [
            "체계적 역량 향상",
            "안정적 업무 수행",
            "팀 내 신뢰 구축",
            "지속적 개선 노력",
            "장기 근속 의지"
        ]
    },
    "at_risk_patterns": {
        "warning_signs": [
            "낮은 참여도",
            "빈번한 질문 반복",
            "소극적 태도",
            "네트워킹 부족",
            "피드백 회피"
        ],
        "intervention_strategies": [
            "1:1 멘토링 강화",
            "학습 방식 조정",
            "소그룹 활동 참여",
            "성공 경험 제공",
            "심리적 안전감 조성"
        ],
        "early_indicators": [
            "첫 주 참여도 50% 미만",
            "질문 빈도 평균 이상",
            "동료 관계 형성 지연",
            "과제 완료율 저조",
            "만족도 점수 3.0 미만"
        ]
    }
}

# === 레거시 Git 워크플로우 템플릿 제거 ===
# 기존 GIT_WORKFLOW_TEMPLATES는 완전히 삭제하고 HRD 온보딩으로 대체

# === 새로운 HRD 온보딩 메인 템플릿 ===
HRD_ONBOARDING_TEMPLATES = COMPREHENSIVE_ONBOARDING_TEMPLATES

# Export for backward compatibility
TEMPLATES = HRD_ONBOARDING_TEMPLATES

if __name__ == "__main__":
    # 템플릿 시스템 테스트
    print("HRD 온보딩 템플릿 시스템 로드 완료")
    print(f"조직 문화 템플릿: {len(ORGANIZATIONAL_CULTURE_TEMPLATES)}개")
    print(f"산업별 템플릿: {len(INDUSTRY_SPECIFIC_TEMPLATES)}개") 
    print(f"직급별 조정: {len(JOB_LEVEL_ADJUSTMENT_TEMPLATES)}개")
    print("\n사용 가능한 조직 문화 유형:")
    for culture_type in ORGANIZATIONAL_CULTURE_TEMPLATES.keys():
        print(f"- {culture_type}: {ORGANIZATIONAL_CULTURE_TEMPLATES[culture_type]['korean']}")
