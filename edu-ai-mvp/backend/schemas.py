
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from enum import Enum

# === Enum을 위한 Pydantic 모델 ===

class IndustryTypeSchema(str, Enum):
    MANUFACTURING = "manufacturing"
    IT_SOFTWARE = "it_software"
    FINANCE = "finance"
    RETAIL = "retail"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    CONSTRUCTION = "construction"
    CONSULTING = "consulting"

class CompanySizeSchema(str, Enum):
    STARTUP = "startup"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class CultureTypeSchema(str, Enum):
    HIERARCHICAL = "hierarchical"
    COLLABORATIVE = "collaborative"
    INNOVATIVE = "innovative"
    RESULTS_ORIENTED = "results"

class LearningStyleSchema(str, Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    READING = "reading"
    KINESTHETIC = "kinesthetic"

class PersonalityTypeSchema(str, Enum):
    ANALYST = "analyst"
    DIPLOMAT = "diplomat"
    SENTINEL = "sentinel"
    EXPLORER = "explorer"

class JobLevelSchema(str, Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"

# === 조직 관련 스키마 ===

class OrganizationBase(BaseModel):
    name: str
    industry: IndustryTypeSchema
    size: CompanySizeSchema
    culture_type: CultureTypeSchema
    core_values: Optional[List[str]] = []
    mission_statement: Optional[str] = None
    vision_statement: Optional[str] = None
    founding_year: Optional[int] = None
    headquarters: Optional[str] = None
    default_onboarding_duration: int = 4
    onboarding_budget_per_person: Optional[int] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# === 신입사원 관련 스키마 ===

class NewHireBase(BaseModel):
    name: str
    email: EmailStr
    job_title: str
    job_level: JobLevelSchema
    start_date: date
    learning_style: Optional[LearningStyleSchema] = None
    personality_type: Optional[PersonalityTypeSchema] = None
    previous_experience_years: int = 0
    education_level: Optional[str] = None
    relevant_skills: Optional[List[str]] = []
    interests: Optional[List[str]] = []

class NewHireCreate(NewHireBase):
    organization_id: int
    department_id: int
    assigned_mentor_id: Optional[int] = None

class NewHireResponse(NewHireBase):
    id: int
    organization_id: int
    department_id: int
    onboarding_status: str
    assigned_mentor_id: Optional[int] = None
    onboarding_start_date: Optional[date] = None
    expected_completion_date: Optional[date] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# === 온보딩 프로그램 관련 스키마 ===

class LearningObjective(BaseModel):
    bloom_level: int  # 1-6
    description: str
    success_criteria: str

class KirkpatrickMetric(BaseModel):
    level: int  # 1-4
    metric_name: str
    measurement_method: str
    target_value: Optional[float] = None

class OnboardingProgramBase(BaseModel):
    title: str
    description: Optional[str] = None
    target_job_roles: List[str]
    target_job_levels: List[JobLevelSchema]
    duration_weeks: int
    estimated_hours: Optional[int] = None
    learning_objectives: Optional[List[LearningObjective]] = []
    kirkpatrick_metrics: Optional[List[KirkpatrickMetric]] = []

class OnboardingProgramCreate(OnboardingProgramBase):
    organization_id: int

class OnboardingProgramResponse(OnboardingProgramBase):
    id: int
    organization_id: int
    is_active: bool
    version: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# === AI 생성 요청 스키마 ===

class OrganizationContextRequest(BaseModel):
    """조직 컨텍스트 정보"""
    organization_id: int
    industry_specifics: Optional[str] = None
    culture_description: Optional[str] = None
    key_challenges: Optional[List[str]] = []

class JobRoleRequest(BaseModel):
    """직무 정보"""
    position: str
    level: JobLevelSchema
    department: str
    key_responsibilities: Optional[List[str]] = []
    required_skills: Optional[List[str]] = []

class LearnerProfileRequest(BaseModel):
    """학습자 개인 정보"""
    learning_style: LearningStyleSchema
    personality_type: PersonalityTypeSchema
    previous_experience_years: int
    education_background: Optional[str] = None
    interests: Optional[List[str]] = []
    learning_preferences: Optional[Dict[str, Any]] = {}

class OnboardingGenerationRequest(BaseModel):
    """AI 온보딩 생성 요청"""
    organization_context: OrganizationContextRequest
    job_role: JobRoleRequest
    learner_profile: LearnerProfileRequest
    duration_weeks: int = 4
    special_requirements: Optional[List[str]] = []
    
    @validator('duration_weeks')
    def validate_duration(cls, v):
        if v < 1 or v > 12:
            raise ValueError('온보딩 기간은 1-12주 사이여야 합니다.')
        return v

# === AI 응답 스키마 ===

class CultureAnalysisResult(BaseModel):
    """조직문화 분석 결과"""
    culture_dimensions: Dict[str, float]  # Hofstede 문화차원 점수
    adaptation_strategies: List[str]
    key_cultural_factors: List[str]
    onboarding_focus_areas: List[str]

class JobOnboardingPlan(BaseModel):
    """직무별 온보딩 계획"""
    learning_path: List[str]
    competency_framework: Dict[str, Any]
    milestone_schedule: Dict[str, str]
    assessment_plan: List[str]

class PersonalizedContent(BaseModel):
    """개인화 콘텐츠"""
    content_modules: List[Dict[str, Any]]
    learning_activities: List[Dict[str, Any]]
    engagement_strategies: List[str]
    personalization_notes: str

class PerformanceTracking(BaseModel):
    """성과 추적 계획"""
    kpi_framework: Dict[str, Any]
    measurement_schedule: Dict[str, str]
    reporting_dashboard: Dict[str, Any]
    improvement_recommendations: List[str]

class OnboardingGenerationResponse(BaseModel):
    """AI 온보딩 생성 응답"""
    message: str
    program_id: int
    culture_analysis: CultureAnalysisResult
    job_onboarding_plan: JobOnboardingPlan  
    personalized_content: PersonalizedContent
    performance_tracking: PerformanceTracking
    estimated_completion_time: int  # 예상 완료 시간(시간)
    success_probability: float      # 성공 확률 예측

# === 분석 및 리포팅 스키마 ===

class OnboardingAnalyticsResponse(BaseModel):
    """온보딩 분석 결과"""
    period_start: date
    period_end: date
    total_new_hires: int
    completion_rate: float
    average_completion_time_days: float
    early_turnover_rate: float
    kirkpatrick_scores: Dict[str, float]
    estimated_roi: float
    department_breakdown: Dict[str, Any]
    recommendations: List[str]
    
    class Config:
        from_attributes = True

# === 대시보드 스키마 ===

class OnboardingDashboardData(BaseModel):
    """HRD 관리자 대시보드 데이터"""
    organization_id: int
    active_new_hires: int
    this_month_hires: int
    completion_rate_trend: List[float]
    satisfaction_trend: List[float]
    upcoming_completions: List[Dict[str, Any]]
    at_risk_hires: List[Dict[str, Any]]  # 이탈 위험 신입사원들
    recent_analytics: OnboardingAnalyticsResponse

class NewHireDashboardData(BaseModel):
    """신입사원 개인 대시보드 데이터"""
    new_hire_id: int
    overall_progress: float
    current_module: Dict[str, Any]
    next_milestones: List[Dict[str, Any]]
    learning_streak: int  # 연속 학습 일수
    achievements: List[str]
    peer_comparison: Dict[str, float]  # 동기들과의 비교 데이터
