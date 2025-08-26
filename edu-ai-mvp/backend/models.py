from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Enum, ForeignKey, Float, Boolean, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

# === Enum 정의 ===

class IndustryType(enum.Enum):
    MANUFACTURING = "manufacturing"
    IT_SOFTWARE = "it_software"
    FINANCE = "finance"
    RETAIL = "retail"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    CONSTRUCTION = "construction"
    CONSULTING = "consulting"

class CompanySize(enum.Enum):
    STARTUP = "startup"          # 1-50명
    SMALL = "small"              # 51-200명  
    MEDIUM = "medium"            # 201-1000명
    LARGE = "large"              # 1001+명

class CultureType(enum.Enum):
    HIERARCHICAL = "hierarchical"    # 위계형
    COLLABORATIVE = "collaborative"  # 협업형
    INNOVATIVE = "innovative"        # 혁신형
    RESULTS_ORIENTED = "results"     # 성과중심형

class LearningStyle(enum.Enum):
    VISUAL = "visual"            # 시각형
    AUDITORY = "auditory"        # 청각형
    READING = "reading"          # 읽기형
    KINESTHETIC = "kinesthetic"  # 체감형

class PersonalityType(enum.Enum):
    # MBTI 간소화 버전
    ANALYST = "analyst"          # NT (분석가형)
    DIPLOMAT = "diplomat"        # NF (외교관형)  
    SENTINEL = "sentinel"        # SJ (관리자형)
    EXPLORER = "explorer"        # SP (탐험가형)

class JobLevel(enum.Enum):
    ENTRY = "entry"              # 신입
    JUNIOR = "junior"            # 주니어 (1-3년)
    MID = "mid"                  # 미드 (3-7년)
    SENIOR = "senior"            # 시니어 (7년+)

# === 핵심 데이터 모델 ===

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    industry = Column(Enum(IndustryType), nullable=False)
    size = Column(Enum(CompanySize), nullable=False)
    culture_type = Column(Enum(CultureType), nullable=False)
    
    # 조직 상세 정보
    core_values = Column(JSON)              # 핵심가치 배열
    mission_statement = Column(Text)         # 미션
    vision_statement = Column(Text)          # 비전
    founding_year = Column(Integer)          # 설립년도
    headquarters = Column(String(100))       # 본사 위치
    
    # 온보딩 설정
    default_onboarding_duration = Column(Integer, default=4)  # 기본 온보딩 기간(주)
    onboarding_budget_per_person = Column(Integer)            # 1인당 온보딩 예산
    
    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 관계
    departments = relationship("Department", back_populates="organization")
    new_hires = relationship("NewHire", back_populates="organization")
    onboarding_programs = relationship("OnboardingProgram", back_populates="organization")

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    head_count = Column(Integer, default=0)
    
    # 부서 특성
    primary_functions = Column(JSON)         # 주요 업무 기능들
    collaboration_departments = Column(JSON) # 협업 부서들
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계
    organization = relationship("Organization", back_populates="departments")
    new_hires = relationship("NewHire", back_populates="department")

class NewHire(Base):
    __tablename__ = "new_hires"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    
    # 기본 정보
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    job_title = Column(String(100), nullable=False)
    job_level = Column(Enum(JobLevel), nullable=False)
    start_date = Column(Date, nullable=False)
    
    # 개인 특성
    learning_style = Column(Enum(LearningStyle))
    personality_type = Column(Enum(PersonalityType))
    previous_experience_years = Column(Integer, default=0)
    education_level = Column(String(50))     # 학력
    relevant_skills = Column(JSON)           # 보유 스킬들
    interests = Column(JSON)                 # 관심사들
    
    # 온보딩 상태
    onboarding_status = Column(String(50), default="assigned")  # assigned, in_progress, completed, dropped_out
    assigned_mentor_id = Column(Integer, ForeignKey('employees.id'))
    onboarding_start_date = Column(Date)
    expected_completion_date = Column(Date)
    actual_completion_date = Column(Date)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 관계
    organization = relationship("Organization", back_populates="new_hires")
    department = relationship("Department", back_populates="new_hires")
    onboarding_records = relationship("OnboardingRecord", back_populates="new_hire")
    mentor = relationship("Employee", foreign_keys=[assigned_mentor_id])

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    job_title = Column(String(100))
    is_mentor = Column(Boolean, default=False)
    mentor_capacity = Column(Integer, default=0)  # 동시 멘토링 가능 인원
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OnboardingProgram(Base):
    __tablename__ = "onboarding_programs"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    
    # 프로그램 기본 정보
    title = Column(String(255), nullable=False)
    description = Column(Text)
    target_job_roles = Column(JSON)          # 대상 직무들
    target_job_levels = Column(JSON)         # 대상 레벨들
    duration_weeks = Column(Integer, nullable=False)
    estimated_hours = Column(Integer)        # 총 예상 학습 시간
    
    # 교육학적 설계
    learning_objectives = Column(JSON)       # Bloom's Taxonomy 기반 학습 목표
    gagne_nine_events = Column(JSON)        # Gagné 9단계 이벤트 구성
    kirkpatrick_metrics = Column(JSON)      # 4단계 평가 지표
    
    # ADDIE 모델 기반 설계 정보
    analysis_results = Column(JSON)         # 분석 결과
    design_principles = Column(JSON)        # 설계 원칙
    development_resources = Column(JSON)    # 개발 리소스
    implementation_plan = Column(JSON)      # 실행 계획
    evaluation_plan = Column(JSON)          # 평가 계획
    
    # 개인화 설정
    supports_learning_styles = Column(JSON) # 지원하는 학습 스타일들
    personalization_features = Column(JSON) # 개인화 기능들
    
    # 상태 및 메타데이터
    is_active = Column(Boolean, default=True)
    version = Column(String(20), default="1.0")
    created_by = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 관계
    organization = relationship("Organization", back_populates="onboarding_programs")
    modules = relationship("LearningModule", back_populates="program")
    records = relationship("OnboardingRecord", back_populates="program")

class LearningModule(Base):
    __tablename__ = "learning_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey('onboarding_programs.id'), nullable=False)
    
    # 모듈 기본 정보
    title = Column(String(255), nullable=False)
    description = Column(Text)
    module_type = Column(String(50))         # orientation, job_training, culture, compliance, etc.
    order_index = Column(Integer, nullable=False)
    
    # 교육학적 분류
    bloom_level = Column(Integer)            # Bloom's Taxonomy 레벨 (1-6)
    gagne_step = Column(Integer)             # Gagné 9단계 중 해당 단계
    learning_style_focus = Column(Enum(LearningStyle))  # 주력 학습 스타일
    
    # 콘텐츠 정보
    content_text = Column(Text)              # 텍스트 콘텐츠
    content_media = Column(JSON)             # 미디어 리소스 (이미지, 비디오 등)
    interactive_elements = Column(JSON)      # 인터랙티브 요소들
    assessments = Column(JSON)               # 평가 문항들
    
    # 학습 설정
    estimated_duration_minutes = Column(Integer)  # 예상 소요 시간
    difficulty_level = Column(Integer)            # 난이도 (1-5)
    prerequisites = Column(JSON)                  # 선수 모듈들
    
    # 개인화 버전들 (JSON으로 다양한 버전 저장)
    personalized_versions = Column(JSON)     # 학습자 특성별 버전들
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 관계
    program = relationship("OnboardingProgram", back_populates="modules")

class OnboardingRecord(Base):
    __tablename__ = "onboarding_records"
    
    id = Column(Integer, primary_key=True, index=True)
    new_hire_id = Column(Integer, ForeignKey('new_hires.id'), nullable=False)
    program_id = Column(Integer, ForeignKey('onboarding_programs.id'), nullable=False)
    
    # 진행 상황
    overall_progress = Column(Float, default=0.0)        # 전체 진행률 (0-100)
    current_module_id = Column(Integer)                  # 현재 학습 중인 모듈
    completed_modules = Column(JSON)                     # 완료된 모듈 ID들
    
    # Kirkpatrick 4단계 평가 점수
    reaction_score = Column(Float)           # Level 1: 만족도 (1-5점)
    learning_score = Column(Float)           # Level 2: 학습 성취도 (0-100점)
    behavior_score = Column(Float)           # Level 3: 업무 적용도 (1-5점)  
    results_impact = Column(Text)            # Level 4: 비즈니스 임팩트 서술
    
    # 학습 분석 데이터
    total_study_time_minutes = Column(Integer, default=0)
    login_count = Column(Integer, default=0)
    interaction_count = Column(Integer, default=0)      # 콘텐츠 상호작용 횟수
    quiz_attempts = Column(JSON)                        # 퀴즈 시도 내역
    feedback_given = Column(Text)                       # 피드백 내용
    
    # 일정 관리
    started_at = Column(DateTime)
    target_completion_date = Column(Date)
    actual_completion_date = Column(DateTime)
    
    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 관계
    new_hire = relationship("NewHire", back_populates="onboarding_records")
    program = relationship("OnboardingProgram", back_populates="records")

# === 성과 분석 및 리포팅 모델 ===

class OnboardingAnalytics(Base):
    __tablename__ = "onboarding_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    
    # 집계 기간
    analysis_period_start = Column(Date, nullable=False)
    analysis_period_end = Column(Date, nullable=False)
    
    # 핵심 지표
    total_new_hires = Column(Integer, default=0)
    completed_onboarding = Column(Integer, default=0)
    dropout_count = Column(Integer, default=0)
    completion_rate = Column(Float)              # 완료율 (%)
    average_completion_time_days = Column(Float) # 평균 완료 시간
    early_turnover_count = Column(Integer, default=0)  # 90일 내 이직자 수
    early_turnover_rate = Column(Float)          # 조기 이직률 (%)
    
    # Kirkpatrick 4단계 평균 점수
    avg_reaction_score = Column(Float)
    avg_learning_score = Column(Float)  
    avg_behavior_score = Column(Float)
    estimated_roi = Column(Float)                # ROI 추정치
    
    # 부서별/직무별 세분화 데이터 (JSON)
    department_breakdown = Column(JSON)
    job_role_breakdown = Column(JSON)
    learning_style_breakdown = Column(JSON)
    
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
