# curriculum_generator.py - HRD 온보딩 커리큘럼 생성기 (완전 리팩토링)

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import models
from onboarding_templates import (
    GAGNE_NINE_EVENTS_ONBOARDING,
    BLOOMS_TAXONOMY_ONBOARDING,
    JOB_ROLE_ONBOARDING_TEMPLATES,
    LEARNING_STYLE_STRATEGIES,
    PERSONALITY_TYPE_STRATEGIES,
    ARCS_MOTIVATION_MODEL,
    INDUSTRY_CUSTOMIZATION
)

class OnboardingCurriculumGenerator:
    """HRD 온보딩 커리큘럼 자동 생성기"""
    
    def __init__(self):
        self.gagne_templates = GAGNE_NINE_EVENTS_ONBOARDING
        self.bloom_templates = BLOOMS_TAXONOMY_ONBOARDING
        self.job_templates = JOB_ROLE_ONBOARDING_TEMPLATES
        self.learning_styles = LEARNING_STYLE_STRATEGIES
        self.personality_types = PERSONALITY_TYPE_STRATEGIES
        self.arcs_model = ARCS_MOTIVATION_MODEL
        self.industry_custom = INDUSTRY_CUSTOMIZATION

    def generate_comprehensive_onboarding(
        self, 
        organization: models.Organization,
        job_role: str,
        job_level: str, 
        learner_profile: Dict[str, Any],
        duration_weeks: int = 4,
        special_requirements: List[str] = None
    ) -> Dict[str, Any]:
        """종합적인 온보딩 프로그램 생성"""
        
        # 1. 조직 컨텍스트 분석
        org_context = self._analyze_organization_context(organization)
        
        # 2. 직무 요구사항 분석
        job_requirements = self._analyze_job_requirements(job_role, job_level)
        
        # 3. 학습자 개인화 프로필
        personalization = self._create_personalization_profile(learner_profile)
        
        # 4. 기본 모듈 생성 (모든 직원 공통)
        common_modules = self._generate_common_modules(org_context, duration_weeks)
        
        # 5. 직무별 전문 모듈
        job_specific_modules = self._generate_job_specific_modules(
            job_role, job_level, job_requirements, duration_weeks
        )
        
        # 6. 개인화 적용
        personalized_modules = self._apply_personalization(
            common_modules + job_specific_modules, 
            personalization
        )
        
        # 7. ARCS 동기 설계 적용
        motivational_design = self._apply_arcs_model(personalized_modules, learner_profile)
        
        # 8. 평가 체계 설계
        assessment_framework = self._design_assessment_framework(
            personalized_modules, job_requirements
        )
        
        # 9. 일정 및 마일스톤
        schedule = self._create_learning_schedule(personalized_modules, duration_weeks)
        
        return {
            "organization_context": org_context,
            "job_requirements": job_requirements,
            "personalization_profile": personalization,
            "learning_modules": personalized_modules,
            "motivational_design": motivational_design,
            "assessment_framework": assessment_framework,
            "learning_schedule": schedule,
            "estimated_total_hours": sum([m.get('duration_hours', 0) for m in personalized_modules]),
            "success_probability": self._calculate_success_probability(learner_profile, org_context),
            "generated_at": datetime.now()
        }

    def _analyze_organization_context(self, organization: models.Organization) -> Dict[str, Any]:
        """조직 컨텍스트 분석"""
        industry_key = organization.industry.value
        culture_key = organization.culture_type.value
        
        return {
            "organization_info": {
                "name": organization.name,
                "industry": industry_key,
                "size": organization.size.value,
                "culture_type": culture_key,
                "core_values": organization.core_values or [],
                "mission": organization.mission_statement,
                "vision": organization.vision_statement
            },
            "industry_characteristics": self.industry_custom.get(industry_key, {}),
            "cultural_factors": {
                "type": culture_key,
                "focus_areas": self._get_culture_focus_areas(culture_key),
                "adaptation_strategies": self._get_culture_adaptation_strategies(culture_key)
            },
            "onboarding_context": {
                "default_duration": organization.default_onboarding_duration,
                "budget_per_person": organization.onboarding_budget_per_person,
                "founding_year": organization.founding_year
            }
        }

    def _analyze_job_requirements(self, job_role: str, job_level: str) -> Dict[str, Any]:
        """직무 요구사항 분석"""
        # 직무를 표준 카테고리로 매핑
        role_category = self._map_job_role_category(job_role)
        
        # 기본 요구사항
        base_requirements = self.job_templates.get(role_category, {})
        
        # 레벨별 조정
        level_adjustments = self._get_level_adjustments(job_level)
        
        return {
            "role": job_role,
            "role_category": role_category,
            "level": job_level,
            "core_competencies": base_requirements.get("core_competencies", []),
            "specific_skills": base_requirements.get("specific_skills", []),
            "learning_priorities": base_requirements.get("learning_priorities", []),
            "success_metrics": base_requirements.get("success_metrics", []),
            "level_adjustments": level_adjustments,
            "estimated_learning_curve": self._estimate_learning_curve(job_role, job_level)
        }

    def _create_personalization_profile(self, learner_profile: Dict[str, Any]) -> Dict[str, Any]:
        """학습자 개인화 프로필 생성"""
        learning_style = learner_profile.get('learning_style', 'visual')
        personality_type = learner_profile.get('personality_type', 'analyst')
        experience_years = learner_profile.get('experience_years', 0)
        
        return {
            "learning_style": {
                "type": learning_style,
                "strategies": self.learning_styles.get(learning_style, {}),
                "content_preferences": self.learning_styles.get(learning_style, {}).get('content_formats', [])
            },
            "personality_type": {
                "type": personality_type,
                "characteristics": self.personality_types.get(personality_type, {}),
                "motivation_factors": self.personality_types.get(personality_type, {}).get('motivation_factors', [])
            },
            "experience_level": {
                "years": experience_years,
                "category": self._categorize_experience(experience_years),
                "adjustments": self._get_experience_adjustments(experience_years)
            },
            "individual_factors": {
                "interests": learner_profile.get('interests', []),
                "preferred_pace": learner_profile.get('preferred_pace', 'normal'),
                "confidence_level": learner_profile.get('confidence_level', 'medium'),
                "learning_goals": learner_profile.get('learning_goals', [])
            }
        }

    def _generate_common_modules(self, org_context: Dict[str, Any], duration_weeks: int) -> List[Dict[str, Any]]:
        """모든 직원 공통 모듈 생성"""
        common_template = self.job_templates["all_roles"]["common_modules"]
        modules = []
        
        for i, template in enumerate(common_template):
            module = {
                "id": f"common_{i+1}",
                "title": template["title"],
                "description": self._generate_module_description(template, org_context),
                "type": "common",
                "duration_hours": template["duration_hours"],
                "bloom_level": template["bloom_level"],
                "gagne_events": template["gagne_events"],
                "content_types": template["content_types"],
                "order_index": i,
                "is_mandatory": True,
                "prerequisites": [],
                "learning_objectives": self._generate_learning_objectives(template, org_context),
                "activities": self._generate_module_activities(template, org_context),
                "assessments": self._generate_module_assessments(template),
                "resources": self._generate_module_resources(template)
            }
            modules.append(module)
        
        return modules

    def _generate_job_specific_modules(
        self, 
        job_role: str, 
        job_level: str, 
        job_requirements: Dict[str, Any], 
        duration_weeks: int
    ) -> List[Dict[str, Any]]:
        """직무별 전문 모듈 생성"""
        role_category = job_requirements["role_category"]
        
        if role_category not in self.job_templates:
            return []
        
        specific_template = self.job_templates[role_category].get("specific_modules", [])
        modules = []
        
        for i, template in enumerate(specific_template):
            # 레벨에 따른 난이도 조정
            adjusted_duration = self._adjust_duration_by_level(
                template["duration_hours"], 
                job_level
            )
            
            module = {
                "id": f"{role_category}_{i+1}",
                "title": template["title"],
                "description": f"{job_role} 전문 과정: {template['title']}",
                "type": "job_specific",
                "job_role": job_role,
                "duration_hours": adjusted_duration,
                "bloom_level": template["bloom_level"],
                "difficulty_level": self._calculate_difficulty_level(template, job_level),
                "key_activities": template.get("key_activities", []),
                "assessment_methods": template.get("assessment", []),
                "order_index": len(modules) + 100,  # 공통 모듈 이후
                "is_mandatory": True,
                "prerequisites": self._determine_prerequisites(template, modules),
                "competencies": self._map_competencies(template, job_requirements),
                "success_criteria": self._define_success_criteria(template, job_requirements)
            }
            modules.append(module)
        
        return modules

    def _apply_personalization(
        self, 
        modules: List[Dict[str, Any]], 
        personalization: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """개인화 적용"""
        learning_style = personalization["learning_style"]["type"]
        personality_type = personalization["personality_type"]["type"]
        experience_level = personalization["experience_level"]["category"]
        
        personalized_modules = []
        
        for module in modules:
            personalized_module = module.copy()
            
            # 학습 스타일에 따른 콘텐츠 형식 조정
            personalized_module["content_formats"] = self._adapt_content_formats(
                module.get("content_types", []), 
                learning_style
            )
            
            # 성격 유형에 따른 접근 방식 조정
            personalized_module["approach"] = self._adapt_approach_by_personality(
                module, 
                personality_type
            )
            
            # 경험 수준에 따른 난이도 조정
            personalized_module["difficulty_adjustment"] = self._adjust_difficulty_by_experience(
                module, 
                experience_level
            )
            
            # 개인별 맞춤 활동 추가
            personalized_module["personalized_activities"] = self._generate_personalized_activities(
                module, 
                personalization
            )
            
            # 학습 경로 추천
            personalized_module["learning_path"] = self._recommend_learning_path(
                module, 
                personalization
            )
            
            personalized_modules.append(personalized_module)
        
        return personalized_modules

    def _apply_arcs_model(
        self, 
        modules: List[Dict[str, Any]], 
        learner_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """ARCS 동기 설계 모델 적용"""
        return {
            "attention_strategies": self._design_attention_strategies(modules, learner_profile),
            "relevance_connections": self._create_relevance_connections(modules, learner_profile),
            "confidence_building": self._design_confidence_building(modules, learner_profile),
            "satisfaction_elements": self._design_satisfaction_elements(modules, learner_profile)
        }

    def _design_assessment_framework(
        self, 
        modules: List[Dict[str, Any]], 
        job_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """평가 체계 설계"""
        return {
            "kirkpatrick_level_1": {
                "reaction_surveys": self._design_reaction_surveys(modules),
                "feedback_mechanisms": ["실시간 피드백", "모듈별 만족도", "개선 제안"]
            },
            "kirkpatrick_level_2": {
                "knowledge_assessments": self._design_knowledge_assessments(modules),
                "skill_demonstrations": self._design_skill_assessments(modules, job_requirements)
            },
            "kirkpatrick_level_3": {
                "behavior_observations": self._design_behavior_assessments(job_requirements),
                "performance_indicators": job_requirements.get("success_metrics", [])
            },
            "kirkpatrick_level_4": {
                "business_impact_metrics": ["생산성 향상", "이직률 감소", "고객 만족도"],
                "roi_calculation": self._design_roi_framework()
            },
            "continuous_assessment": {
                "formative_assessments": "진행 중 평가",
                "summative_assessments": "최종 평가",
                "peer_evaluations": "동료 평가",
                "self_assessments": "자가 평가"
            }
        }

    def _create_learning_schedule(
        self, 
        modules: List[Dict[str, Any]], 
        duration_weeks: int
    ) -> Dict[str, Any]:
        """학습 일정 생성"""
        total_hours = sum([m.get('duration_hours', 0) for m in modules])
        hours_per_week = total_hours / duration_weeks if duration_weeks > 0 else 20
        
        weekly_schedule = {}
        current_week = 1
        current_hours = 0
        
        for module in sorted(modules, key=lambda x: x.get('order_index', 999)):
            module_hours = module.get('duration_hours', 0)
            
            if current_hours + module_hours > hours_per_week and current_week < duration_weeks:
                current_week += 1
                current_hours = 0
            
            if f"week_{current_week}" not in weekly_schedule:
                weekly_schedule[f"week_{current_week}"] = []
            
            weekly_schedule[f"week_{current_week}"].append({
                "module_id": module["id"],
                "module_title": module["title"],
                "duration_hours": module_hours,
                "type": module["type"]
            })
            
            current_hours += module_hours
        
        return {
            "total_duration_weeks": duration_weeks,
            "total_hours": total_hours,
            "hours_per_week": hours_per_week,
            "weekly_breakdown": weekly_schedule,
            "milestones": self._create_milestones(weekly_schedule, duration_weeks),
            "checkpoints": self._create_checkpoints(duration_weeks)
        }

    # === 헬퍼 메서드들 ===
    
    def _map_job_role_category(self, job_role: str) -> str:
        """직무를 표준 카테고리로 매핑"""
        role_lower = job_role.lower()
        
        if any(term in role_lower for term in ['develop', 'engineer', 'programmer', 'dev']):
            return 'engineering'
        elif any(term in role_lower for term in ['sales', 'account', 'business']):
            return 'sales'
        elif any(term in role_lower for term in ['marketing', 'promotion', 'brand']):
            return 'marketing'
        elif any(term in role_lower for term in ['hr', 'human', 'recruit', 'talent']):
            return 'hr'
        else:
            return 'all_roles'

    def _calculate_success_probability(
        self, 
        learner_profile: Dict[str, Any], 
        org_context: Dict[str, Any]
    ) -> float:
        """성공 확률 계산"""
        base_probability = 0.75
        
        # 경험 수준 가산점
        experience = learner_profile.get('experience_years', 0)
        if experience > 5:
            base_probability += 0.1
        elif experience > 2:
            base_probability += 0.05
        elif experience == 0:
            base_probability -= 0.05
            
        # 학습 스타일과 성격 유형 매칭
        learning_style = learner_profile.get('learning_style', '')
        personality = learner_profile.get('personality_type', '')
        culture_type = org_context.get('organization_info', {}).get('culture_type', '')
        
        # 문화 적합성
        if culture_type == 'innovative' and personality in ['analyst', 'explorer']:
            base_probability += 0.08
        elif culture_type == 'collaborative' and personality in ['diplomat', 'sentinel']:
            base_probability += 0.08
            
        return min(0.95, max(0.50, base_probability))

    def _get_culture_focus_areas(self, culture_type: str) -> List[str]:
        """문화 유형별 집중 영역"""
        focus_map = {
            'hierarchical': ['조직 구조', '권한과 책임', '보고 체계', '절차 준수'],
            'collaborative': ['팀워크', '소통', '상호 협력', '집단 의사결정'],
            'innovative': ['창의성', '변화 수용', '실험 정신', '학습 문화'],
            'results': ['성과 지향', '목표 달성', '효율성', '경쟁력']
        }
        return focus_map.get(culture_type, ['기본 조직 이해'])

    def _estimate_learning_curve(self, job_role: str, job_level: str) -> Dict[str, int]:
        """학습 곡선 추정"""
        base_days = {'entry': 45, 'junior': 30, 'mid': 21, 'senior': 14}
        role_multiplier = {
            'engineering': 1.2,
            'sales': 1.0,
            'marketing': 0.9,
            'hr': 1.1
        }
        
        role_category = self._map_job_role_category(job_role)
        base = base_days.get(job_level, 30)
        multiplier = role_multiplier.get(role_category, 1.0)
        
        return {
            'basic_productivity': int(base * 0.5 * multiplier),
            'full_productivity': int(base * multiplier),
            'expert_level': int(base * 2 * multiplier)
        }

    # 기타 헬퍼 메서드들... (간소화를 위해 일부 생략)
    def _generate_module_description(self, template, org_context): return f"{template['title']} - 조직 맞춤형"
    def _generate_learning_objectives(self, template, org_context): return ["목표1", "목표2"]
    def _generate_module_activities(self, template, org_context): return ["활동1", "활동2"] 
    def _generate_module_assessments(self, template): return ["평가1", "평가2"]
    def _generate_module_resources(self, template): return ["리소스1", "리소스2"]
    def _adjust_duration_by_level(self, base_hours, level): return base_hours * {'entry': 1.2, 'junior': 1.0, 'mid': 0.9, 'senior': 0.8}.get(level, 1.0)
    def _calculate_difficulty_level(self, template, level): return {'entry': 2, 'junior': 3, 'mid': 4, 'senior': 5}.get(level, 3)
    def _determine_prerequisites(self, template, modules): return []
    def _map_competencies(self, template, requirements): return requirements.get('core_competencies', [])
    def _define_success_criteria(self, template, requirements): return requirements.get('success_metrics', [])

# === 사용 예시 ===
if __name__ == "__main__":
    generator = OnboardingCurriculumGenerator()
    
    # 샘플 데이터
    sample_org = models.Organization(
        name="테크이노베이션",
        industry="it_software", 
        size="medium",
        culture_type="innovative"
    )
    
    sample_profile = {
        'learning_style': 'visual',
        'personality_type': 'analyst', 
        'experience_years': 3,
        'interests': ['AI', 'ML', 'DevOps']
    }
    
    result = generator.generate_comprehensive_onboarding(
        organization=sample_org,
        job_role="Software Engineer",
        job_level="junior",
        learner_profile=sample_profile,
        duration_weeks=4
    )
    
    print("Generated onboarding program:")
    print(f"Total modules: {len(result['learning_modules'])}")
    print(f"Total hours: {result['estimated_total_hours']}")
    print(f"Success probability: {result['success_probability']:.1%}")
