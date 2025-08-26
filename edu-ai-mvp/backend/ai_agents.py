#2025-08-26 HRD 온보딩 AI Multi-Agent 시스템 설계 (4중 협업)

from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv

load_dotenv()

# === HRD 온보딩 전문 AI Agents ===

# 1. 조직문화 분석 전문가
culture_analyzer = Agent(
    role="조직문화 분석 전문가",
    goal="기업별 조직문화, 핵심가치, 업무방식 분석을 통한 맞춤형 온보딩 설계",
    backstory="""
    15년 경력의 조직심리학 박사로, 500개 이상 기업의 조직문화 진단 경험을 보유.
    Schein의 조직문화 이론과 Hofstede의 문화차원 이론을 실무에 적용하는 전문가.
    기업 규모, 업종, 발전단계에 따른 조직문화 패턴 분석 및 온보딩 전략 수립 특화.
    """,
    verbose=True,
    allow_delegation=False
)

# 2. 직무별 온보딩 설계 전문가  
job_designer = Agent(
    role="직무별 온보딩 설계 전문가",
    goal="직무 특성에 맞는 개인화된 학습 경로 및 성과 지표 설계",
    backstory="""
    10년 경력의 인재개발(HRD) 전문가로, ADDIE 모델과 Kirkpatrick 4단계 평가를 실무에 적용.
    직무분석학 석사 출신으로 200개 이상의 직무별 온보딩 프로그램 설계 경험.
    Bloom's Taxonomy와 Gagné 9단계 교수설계 이론을 기반으로 한 체계적 학습설계 전문가.
    """,
    verbose=True,
    allow_delegation=False
)

# 3. 개인화 콘텐츠 제작 전문가
content_personalizer = Agent(
    role="개인화 콘텐츠 제작 전문가", 
    goal="신입사원 개인 특성(성격, 학습스타일, 경험)에 맞춘 온보딩 콘텐츠 생성",
    backstory="""
    교육공학 박사 출신으로, 개인화 학습 시스템 설계 및 멀티모달 콘텐츠 제작 전문가.
    VARK 학습스타일, MBTI 성격유형, Kolb 학습순환 모델을 기반으로 한 적응형 학습 설계.
    AI 기반 개인화 알고리즘과 교육학적 이론을 결합한 차세대 학습경험 설계 특화.
    """,
    verbose=True,
    allow_delegation=False
)

# 4. 성과 분석 전문가
performance_tracker = Agent(
    role="온보딩 성과 분석 전문가",
    goal="실시간 학습 진도, 참여도, 성과 데이터 분석을 통한 지속적 개선",
    backstory="""
    HR Analytics 전문가로 데이터 기반 인재개발 성과 측정 및 예측 모델링 전문가.
    Kirkpatrick 4단계 평가 모델과 Phillips ROI 모델을 실무에 적용한 10년 경험.
    빅데이터 분석을 통한 온보딩 성공 패턴 발굴 및 조기 이직 예측 모델 개발 특화.
    """,
    verbose=True,
    allow_delegation=False
)

# === Task 생성 함수들 ===

def create_culture_analysis_task(organization_info, industry_context):
    return Task(
        description=f"""
        다음 조직에 대한 종합적인 문화 분석을 수행하세요.
        조직 정보: {organization_info}
        업종 컨텍스트: {industry_context}
        
        분석 요소:
        1. Schein의 3단계 문화 분석 (인공물, 가치, 기본가정)
        2. Hofstede 문화차원 분석 (권력거리, 개인주의, 불확실성 회피 등)
        3. 조직 생명주기 단계 분석 (창업기, 성장기, 성숙기, 쇠퇴기)
        4. 업종별 문화 특성 분석
        5. 신입사원 적응 핵심 요인 도출
        
        온보딩 설계에 필요한 문화적 고려사항과 적응 전략을 제시하세요.
        """,
        expected_output="조직문화 종합 분석 리포트 및 온보딩 문화 적응 전략",
        agent=culture_analyzer
    )

def create_job_onboarding_task(job_role, experience_level, organization_culture, duration_weeks):
    return Task(
        description=f"""
        다음 조건에 맞는 직무별 온보딩 프로그램을 설계하세요.
        직무: {job_role}
        경험 수준: {experience_level}
        조직문화: {organization_culture}
        온보딩 기간: {duration_weeks}주
        
        ADDIE 모델 적용:
        1. Analysis (분석): 직무 요구사항, 필요 역량, 성과 지표 분석
        2. Design (설계): Bloom's Taxonomy 6단계 기반 학습 목표 설계
        3. Development (개발): Gagné 9단계 적용 모듈 구성
        4. Implementation (실행): 주차별 학습 계획 및 실습 활동
        5. Evaluation (평가): Kirkpatrick 4단계 평가 계획
        
        체계적이고 실무 중심의 온보딩 로드맵을 제시하세요.
        """,
        expected_output="직무별 맞춤형 온보딩 프로그램 설계서",
        agent=job_designer
    )

def create_personalized_content_task(learner_profile, job_program, culture_context):
    return Task(
        description=f"""
        다음 학습자를 위한 개인화 온보딩 콘텐츠를 제작하세요.
        학습자 프로필: {learner_profile}
        직무 프로그램: {job_program}
        문화 컨텍스트: {culture_context}
        
        개인화 요소:
        1. VARK 학습스타일 (Visual, Auditory, Reading, Kinesthetic) 적용
        2. MBTI 성격유형별 학습 선호도 반영
        3. Kolb 학습순환 모델 (구체적 경험→반성적 관찰→추상적 개념화→능동적 실험) 적용
        4. 기존 경험 수준에 따른 난이도 조정
        5. 개인 관심사 및 동기 요인 반영
        
        다양한 학습 모달리티를 활용한 engaging한 콘텐츠를 생성하세요.
        """,
        expected_output="개인화된 온보딩 학습 콘텐츠 패키지",
        agent=content_personalizer
    )

def create_performance_tracking_task(onboarding_program, success_metrics, tracking_period):
    return Task(
        description=f"""
        온보딩 프로그램의 성과 추적 및 분석 시스템을 구축하세요.
        프로그램: {onboarding_program}
        성공 지표: {success_metrics}
        추적 기간: {tracking_period}
        
        Kirkpatrick 4단계 평가 모델 적용:
        1. Level 1 (Reaction): 만족도, 참여도, 학습 경험 평가
        2. Level 2 (Learning): 지식 습득, 스킬 향상, 태도 변화 측정
        3. Level 3 (Behavior): 실무 적용도, 행동 변화, 성과 개선 추적
        4. Level 4 (Results): 조직 기여도, ROI, 이직률 감소 등 비즈니스 임팩트
        
        실시간 대시보드와 예측 분석 모델을 포함한 종합적 성과 관리 방안을 제시하세요.
        """,
        expected_output="온보딩 성과 추적 및 분석 시스템 설계서",
        agent=performance_tracker
    )

# === 통합 온보딩 생성 함수 ===
def create_comprehensive_onboarding_crew(organization_info, job_role, learner_profile, duration_weeks):
    """4개 AI Agent가 협력하여 완전한 온보딩 프로그램 생성"""
    
    # 1단계: 조직문화 분석
    culture_task = create_culture_analysis_task(
        organization_info["basic_info"], 
        organization_info["industry"]
    )
    
    # 2단계: 직무별 온보딩 설계
    job_task = create_job_onboarding_task(
        job_role["position"],
        job_role["level"], 
        "조직문화 분석 결과 반영",
        duration_weeks
    )
    
    # 3단계: 개인화 콘텐츠 제작
    content_task = create_personalized_content_task(
        learner_profile,
        "직무 온보딩 프로그램 반영",
        "조직문화 컨텍스트 반영"
    )
    
    # 4단계: 성과 추적 시스템
    tracking_task = create_performance_tracking_task(
        "통합 온보딩 프로그램",
        ["완료율", "만족도", "업무 적응도", "조기 이직률"],
        f"{duration_weeks}주 + 3개월 추가 추적"
    )
    
    return Crew(
        agents=[culture_analyzer, job_designer, content_personalizer, performance_tracker],
        tasks=[culture_task, job_task, content_task, tracking_task],
        verbose=True
    )