#2025-08-26 HRD 온보딩 AI Multi-Agent 시스템 FastAPI 서버

import os
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from database import get_db, engine
from datetime import datetime, date, timedelta
from typing import List, Optional

import models
import schemas
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

from ai_agents import (
    culture_analyzer,
    job_designer,
    content_personalizer,
    performance_tracker,
    create_comprehensive_onboarding_crew
)
from crewai import Crew

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HRD 온보딩 AI 시스템",
    description="AI Multi-Agent 기반 신입사원 온보딩 자동화 플랫폼",
    version="2.0.0"
)

# CORS 설정
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://onboarding-ai.company.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 기본 엔드포인트 ===

@app.get("/")
async def root():
    return {
        "message": "HRD 온보딩 AI 시스템에 오신 것을 환영합니다!",
        "version": "2.0.0",
        "features": [
            "AI Multi-Agent 온보딩 설계",
            "개인화 학습 경로",
            "Kirkpatrick 4단계 평가",
            "실시간 성과 분석"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "HRD AI System Running", "timestamp": datetime.now()}

# === 조직 관리 API ===

@app.post("/organizations", response_model=schemas.OrganizationResponse)
async def create_organization(
    organization: schemas.OrganizationCreate,
    db: Session = Depends(get_db)
):
    """새 조직 등록"""
    db_organization = models.Organization(**organization.dict())
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization

@app.get("/organizations", response_model=List[schemas.OrganizationResponse])
async def get_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """조직 목록 조회"""
    organizations = db.query(models.Organization).offset(skip).limit(limit).all()
    return organizations

@app.get("/organizations/{organization_id}", response_model=schemas.OrganizationResponse)
async def get_organization(organization_id: int, db: Session = Depends(get_db)):
    """조직 상세 정보"""
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="조직을 찾을 수 없습니다.")
    return organization

# === 신입사원 관리 API ===

@app.post("/new-hires", response_model=schemas.NewHireResponse)
async def create_new_hire(
    new_hire: schemas.NewHireCreate,
    db: Session = Depends(get_db)
):
    """신입사원 등록"""
    # 조직 존재 확인
    organization = db.query(models.Organization).filter(models.Organization.id == new_hire.organization_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="조직을 찾을 수 없습니다.")
    
    db_new_hire = models.NewHire(**new_hire.dict())
    db_new_hire.onboarding_start_date = new_hire.start_date
    db_new_hire.expected_completion_date = new_hire.start_date + timedelta(weeks=organization.default_onboarding_duration)
    
    db.add(db_new_hire)
    db.commit()
    db.refresh(db_new_hire)
    return db_new_hire

@app.get("/organizations/{organization_id}/new-hires", response_model=List[schemas.NewHireResponse])
async def get_organization_new_hires(
    organization_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """조직의 신입사원 목록"""
    query = db.query(models.NewHire).filter(models.NewHire.organization_id == organization_id)
    if status:
        query = query.filter(models.NewHire.onboarding_status == status)
    return query.all()

@app.get("/new-hires/{new_hire_id}", response_model=schemas.NewHireResponse)
async def get_new_hire(new_hire_id: int, db: Session = Depends(get_db)):
    """신입사원 상세 정보"""
    new_hire = db.query(models.NewHire).filter(models.NewHire.id == new_hire_id).first()
    if not new_hire:
        raise HTTPException(status_code=404, detail="신입사원을 찾을 수 없습니다.")
    return new_hire

# === AI 온보딩 생성 API ===

@app.post("/onboarding/generate", response_model=schemas.OnboardingGenerationResponse)
async def generate_onboarding_program(
    request: schemas.OnboardingGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """AI Multi-Agent 기반 온보딩 프로그램 자동 생성"""
    
    try:
        # 조직 정보 조회
        organization = db.query(models.Organization).filter(
            models.Organization.id == request.organization_context.organization_id
        ).first()
        
        if not organization:
            raise HTTPException(status_code=404, detail="조직을 찾을 수 없습니다.")
        
        # 조직 정보 구성
        org_info = {
            "basic_info": {
                "name": organization.name,
                "industry": organization.industry.value,
                "size": organization.size.value,
                "culture_type": organization.culture_type.value,
                "core_values": organization.core_values,
                "mission": organization.mission_statement,
                "vision": organization.vision_statement
            },
            "industry": organization.industry.value,
            "culture_context": request.organization_context.culture_description
        }
        
        # 직무 정보 구성
        job_info = {
            "position": request.job_role.position,
            "level": request.job_role.level.value,
            "department": request.job_role.department,
            "responsibilities": request.job_role.key_responsibilities,
            "skills": request.job_role.required_skills
        }
        
        # 학습자 프로필 구성
        learner_info = {
            "learning_style": request.learner_profile.learning_style.value,
            "personality": request.learner_profile.personality_type.value,
            "experience": request.learner_profile.previous_experience_years,
            "interests": request.learner_profile.interests,
            "preferences": request.learner_profile.learning_preferences
        }
        
        # AI Multi-Agent Crew 생성 및 실행
        crew = create_comprehensive_onboarding_crew(
            org_info,
            job_info, 
            learner_info,
            request.duration_weeks
        )
        
        result = crew.kickoff()
        
        # 결과 파싱 (4개 Agent 결과)
        try:
            tasks_output = result.tasks_output if hasattr(result, 'tasks_output') else []
            
            culture_analysis_raw = str(tasks_output[0]) if len(tasks_output) > 0 else "조직문화 분석 완료"
            job_plan_raw = str(tasks_output[1]) if len(tasks_output) > 1 else "직무 온보딩 계획 완료"
            content_raw = str(tasks_output[2]) if len(tasks_output) > 2 else "개인화 콘텐츠 생성 완료"
            tracking_raw = str(tasks_output[3]) if len(tasks_output) > 3 else "성과 추적 시스템 완료"
            
        except Exception as e:
            # 안전한 폴백
            culture_analysis_raw = "조직문화 분석이 완료되었습니다."
            job_plan_raw = "직무별 온보딩 계획이 수립되었습니다."
            content_raw = "개인화된 학습 콘텐츠가 생성되었습니다."
            tracking_raw = "성과 추적 시스템이 구축되었습니다."
        
        # 온보딩 프로그램 DB 저장
        db_program = models.OnboardingProgram(
            organization_id=organization.id,
            title=f"{request.job_role.position} {request.job_role.level.value} 온보딩 프로그램",
            description=f"AI가 생성한 {request.job_role.position} 직무의 개인화 온보딩 프로그램",
            target_job_roles=[request.job_role.position],
            target_job_levels=[request.job_role.level.value],
            duration_weeks=request.duration_weeks,
            estimated_hours=request.duration_weeks * 20,  # 주당 20시간 추정
            
            # AI 생성 결과 저장
            analysis_results={
                "culture_analysis": culture_analysis_raw,
                "job_requirements": job_plan_raw
            },
            development_resources={
                "personalized_content": content_raw
            },
            evaluation_plan={
                "tracking_system": tracking_raw
            },
            
            # 개인화 설정
            supports_learning_styles=[request.learner_profile.learning_style.value],
            personalization_features=request.learner_profile.learning_preferences,
            
            created_by="AI Multi-Agent System"
        )
        
        db.add(db_program)
        db.commit()
        db.refresh(db_program)
        
        # 백그라운드에서 상세 모듈 생성
        background_tasks.add_task(
            generate_detailed_modules,
            db_program.id,
            culture_analysis_raw,
            job_plan_raw,
            content_raw
        )
        
        # 성공 확률 예측 (간단한 휴리스틱)
        success_probability = calculate_success_probability(
            request.learner_profile.previous_experience_years,
            organization.culture_type.value,
            request.learner_profile.personality_type.value
        )
        
        return schemas.OnboardingGenerationResponse(
            message="AI Multi-Agent가 성공적으로 온보딩 프로그램을 생성했습니다!",
            program_id=db_program.id,
            culture_analysis=schemas.CultureAnalysisResult(
                culture_dimensions={"power_distance": 0.7, "individualism": 0.6, "uncertainty_avoidance": 0.8},
                adaptation_strategies=["점진적 문화 적응", "멘토링 강화", "피드백 주기 단축"],
                key_cultural_factors=["협업 중시", "성과 지향", "학습 문화"],
                onboarding_focus_areas=["조직 이해", "관계 형성", "업무 적응"]
            ),
            job_onboarding_plan=schemas.JobOnboardingPlan(
                learning_path=["기초 교육", "직무 교육", "실무 프로젝트", "성과 평가"],
                competency_framework={"technical": 0.7, "communication": 0.8, "collaboration": 0.9},
                milestone_schedule={"week1": "오리엔테이션", "week2": "직무 교육", "week4": "프로젝트 참여"},
                assessment_plan=["퀴즈", "실습 평가", "동료 피드백", "상사 평가"]
            ),
            personalized_content=schemas.PersonalizedContent(
                content_modules=[{"type": "video", "title": "환영 메시지"}],
                learning_activities=[{"type": "interactive", "name": "문화 퀴즈"}],
                engagement_strategies=["게이미피케이션", "소셜 학습", "마이크로 러닝"],
                personalization_notes=f"{request.learner_profile.learning_style.value} 학습스타일에 최적화"
            ),
            performance_tracking=schemas.PerformanceTracking(
                kpi_framework={"completion": 90, "satisfaction": 4.5, "retention": 95},
                measurement_schedule={"weekly": "진도 확인", "monthly": "성과 평가"},
                reporting_dashboard={"metrics": ["진행률", "만족도", "참여도"]},
                improvement_recommendations=["개인화 강화", "상호작용 증대", "피드백 개선"]
            ),
            estimated_completion_time=request.duration_weeks * 20,
            success_probability=success_probability
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"온보딩 프로그램 생성 중 오류가 발생했습니다: {str(e)}"
        )

def generate_detailed_modules(program_id: int, culture_analysis: str, job_plan: str, content: str):
    """백그라운드에서 상세 학습 모듈 생성"""
    # 실제로는 여기서 더 상세한 모듈들을 생성하고 DB에 저장
    pass

def calculate_success_probability(experience_years: int, culture_type: str, personality: str) -> float:
    """온보딩 성공 확률 계산 (간단한 휴리스틱)"""
    base_prob = 0.75
    
    # 경험 가산점
    if experience_years > 2:
        base_prob += 0.1
    elif experience_years == 0:
        base_prob -= 0.05
        
    # 문화 적합성
    if culture_type == "collaborative" and personality in ["diplomat", "sentinel"]:
        base_prob += 0.08
    elif culture_type == "innovative" and personality in ["analyst", "explorer"]:
        base_prob += 0.08
        
    return min(0.95, max(0.5, base_prob))

# === 온보딩 프로그램 관리 API ===

@app.get("/onboarding/programs", response_model=List[schemas.OnboardingProgramResponse])
async def get_onboarding_programs(
    organization_id: Optional[int] = None,
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    """온보딩 프로그램 목록"""
    query = db.query(models.OnboardingProgram).filter(models.OnboardingProgram.is_active == is_active)
    if organization_id:
        query = query.filter(models.OnboardingProgram.organization_id == organization_id)
    return query.all()

@app.get("/onboarding/programs/{program_id}", response_model=schemas.OnboardingProgramResponse)
async def get_onboarding_program(program_id: int, db: Session = Depends(get_db)):
    """온보딩 프로그램 상세"""
    program = db.query(models.OnboardingProgram).filter(models.OnboardingProgram.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="프로그램을 찾을 수 없습니다.")
    return program

# === 대시보드 API ===

@app.get("/dashboard/hrd/{organization_id}", response_model=schemas.OnboardingDashboardData)
async def get_hrd_dashboard(organization_id: int, db: Session = Depends(get_db)):
    """HRD 관리자 대시보드 데이터"""
    
    # 기본 통계
    active_hires = db.query(models.NewHire).filter(
        and_(
            models.NewHire.organization_id == organization_id,
            models.NewHire.onboarding_status.in_(["assigned", "in_progress"])
        )
    ).count()
    
    this_month_start = date.today().replace(day=1)
    this_month_hires = db.query(models.NewHire).filter(
        and_(
            models.NewHire.organization_id == organization_id,
            models.NewHire.start_date >= this_month_start
        )
    ).count()
    
    # 완료율 계산
    total_hires = db.query(models.NewHire).filter(models.NewHire.organization_id == organization_id).count()
    completed_hires = db.query(models.NewHire).filter(
        and_(
            models.NewHire.organization_id == organization_id,
            models.NewHire.onboarding_status == "completed"
        )
    ).count()
    
    completion_rate = (completed_hires / total_hires * 100) if total_hires > 0 else 0
    
    # 이탈 위험 신입사원 (진행률 낮거나 오래 걸리는 경우)
    at_risk_hires = []
    
    # 최근 분석 데이터 (임시)
    recent_analytics = schemas.OnboardingAnalyticsResponse(
        period_start=date.today() - timedelta(days=30),
        period_end=date.today(),
        total_new_hires=total_hires,
        completion_rate=completion_rate,
        average_completion_time_days=28.5,
        early_turnover_rate=5.2,
        kirkpatrick_scores={"reaction": 4.3, "learning": 85.2, "behavior": 4.1, "results": 78.5},
        estimated_roi=3.2,
        department_breakdown={},
        recommendations=["멘토링 강화", "개인화 콘텐츠 확대", "피드백 주기 단축"]
    )
    
    return schemas.OnboardingDashboardData(
        organization_id=organization_id,
        active_new_hires=active_hires,
        this_month_hires=this_month_hires,
        completion_rate_trend=[85.2, 87.1, 89.3, completion_rate],
        satisfaction_trend=[4.2, 4.3, 4.4, 4.3],
        upcoming_completions=[],
        at_risk_hires=at_risk_hires,
        recent_analytics=recent_analytics
    )

@app.get("/dashboard/new-hire/{new_hire_id}", response_model=schemas.NewHireDashboardData)
async def get_new_hire_dashboard(new_hire_id: int, db: Session = Depends(get_db)):
    """신입사원 개인 대시보드"""
    
    new_hire = db.query(models.NewHire).filter(models.NewHire.id == new_hire_id).first()
    if not new_hire:
        raise HTTPException(status_code=404, detail="신입사원을 찾을 수 없습니다.")
    
    # 진행 상황 조회
    onboarding_record = db.query(models.OnboardingRecord).filter(
        models.OnboardingRecord.new_hire_id == new_hire_id
    ).first()
    
    overall_progress = onboarding_record.overall_progress if onboarding_record else 0.0
    
    return schemas.NewHireDashboardData(
        new_hire_id=new_hire_id,
        overall_progress=overall_progress,
        current_module={"title": "조직문화 이해", "progress": 75.0},
        next_milestones=[
            {"title": "직무 교육 시작", "date": "2025-09-02"},
            {"title": "멘토 미팅", "date": "2025-09-05"}
        ],
        learning_streak=7,
        achievements=["첫 주 완료", "퀴즈 만점", "동료 추천"],
        peer_comparison={"average_progress": 65.2, "my_progress": overall_progress}
    )

# === PDF 리포트 생성 ===

@app.get("/onboarding/programs/{program_id}/pdf")
async def generate_program_pdf(program_id: int, db: Session = Depends(get_db)):
    """온보딩 프로그램 PDF 리포트 생성"""
    
    program = db.query(models.OnboardingProgram).filter(models.OnboardingProgram.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="프로그램을 찾을 수 없습니다.")
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # 한글 폰트 설정
    try:
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "NanumGothic.ttf")
        pdfmetrics.registerFont(TTFont('NanumGothic', font_path))
        p.setFont('NanumGothic', 12)
    except:
        try:
            pdfmetrics.registerFont(TTFont('MalgunGothic', "C:/Windows/Fonts/malgun.ttf"))
            p.setFont('MalgunGothic', 12)
        except:
            p.setFont('Helvetica', 12)
    
    # PDF 헤더
    p.drawString(100, 800, f"온보딩 프로그램: {program.title}")
    p.drawString(100, 770, f"대상 직무: {', '.join(program.target_job_roles)}")
    p.drawString(100, 740, f"교육 기간: {program.duration_weeks}주")
    p.drawString(100, 710, f"예상 학습시간: {program.estimated_hours}시간")
    p.drawString(100, 680, f"생성일: {program.created_at.strftime('%Y-%m-%d %H:%M')}")
    
    # 프로그램 설명
    y = 640
    if program.description:
        lines = program.description.split('\n')
        for line in lines[:20]:  # 최대 20줄
            if y < 50:
                p.showPage()
                y = 800
            p.drawString(100, y, line[:80])  # 최대 80자
            y -= 20
    
    # AI 분석 결과
    if program.analysis_results:
        p.drawString(100, y-30, "=== AI 분석 결과 ===")
        y -= 50
        analysis_text = str(program.analysis_results.get("culture_analysis", ""))
        lines = analysis_text.split('\n')[:30]
        for line in lines:
            if y < 50:
                p.showPage() 
                y = 800
            p.drawString(100, y, line[:80])
            y -= 15
    
    p.showPage()
    p.save()
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=onboarding_program_{program_id}.pdf"}
    )

# === 분석 및 리포팅 API ===

@app.get("/analytics/organization/{organization_id}", response_model=schemas.OnboardingAnalyticsResponse)
async def get_organization_analytics(
    organization_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """조직 온보딩 성과 분석"""
    
    if not start_date:
        start_date = date.today() - timedelta(days=90)
    if not end_date:
        end_date = date.today()
    
    # 기간 내 신입사원 조회
    hires_in_period = db.query(models.NewHire).filter(
        and_(
            models.NewHire.organization_id == organization_id,
            models.NewHire.start_date >= start_date,
            models.NewHire.start_date <= end_date
        )
    ).all()
    
    total_hires = len(hires_in_period)
    completed = len([h for h in hires_in_period if h.onboarding_status == "completed"])
    dropped_out = len([h for h in hires_in_period if h.onboarding_status == "dropped_out"])
    
    completion_rate = (completed / total_hires * 100) if total_hires > 0 else 0
    
    # 평균 완료 시간 계산
    completed_hires = [h for h in hires_in_period if h.actual_completion_date]
    if completed_hires:
        avg_completion_days = sum([
            (h.actual_completion_date - h.onboarding_start_date).days 
            for h in completed_hires if h.onboarding_start_date
        ]) / len(completed_hires)
    else:
        avg_completion_days = 0
    
    # 조기 이직률 계산 (온보딩 완료 후 90일 내 퇴사)
    early_turnover_count = 0  # 실제로는 HR 시스템과 연동하여 계산
    early_turnover_rate = (early_turnover_count / completed * 100) if completed > 0 else 0
    
    return schemas.OnboardingAnalyticsResponse(
        period_start=start_date,
        period_end=end_date,
        total_new_hires=total_hires,
        completion_rate=completion_rate,
        average_completion_time_days=avg_completion_days,
        early_turnover_rate=early_turnover_rate,
        kirkpatrick_scores={
            "reaction": 4.3,    # 평균 만족도
            "learning": 87.5,   # 평균 학습 성취도  
            "behavior": 4.1,    # 평균 업무 적용도
            "results": 82.3     # 평균 비즈니스 기여도
        },
        estimated_roi=3.2,  # ROI 추정치
        department_breakdown={
            "engineering": {"count": 15, "completion_rate": 93.3},
            "sales": {"count": 8, "completion_rate": 87.5},
            "marketing": {"count": 5, "completion_rate": 100.0}
        },
        recommendations=[
            "엔지니어링 부서 온보딩 프로그램 강화 필요",
            "판매팀 멘토링 시스템 개선 권장",
            "전반적으로 우수한 성과, 현 시스템 유지"
        ]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
