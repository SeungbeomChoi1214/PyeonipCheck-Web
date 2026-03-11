# 단기 해결책: API 레벨 방어 로직 (main_improved.py)

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator
from typing import List, Optional

# 개선된 Response 모델
class DepartmentResponse(BaseModel):
    id: int
    name: str
    division: str
    exam_type: str
    university_name: str  # 추가: 소속 대학명 명시
    full_identifier: str  # 추가: 고유 식별자
    
    class Config:
        from_attributes = True

class PredictRequest(BaseModel):
    dept_id: int
    university_id: int  # 추가: 대학 ID 검증용
    my_score_eng: float
    my_score_math: float = 0.0
    
    @validator('dept_id')
    def validate_dept_id(cls, v):
        if v <= 0:
            raise ValueError('Invalid department ID')
        return v

# 개선된 API 엔드포인트
@app.get("/universities/{univ_id}/departments", response_model=List[DepartmentResponse])
def get_departments(univ_id: int, db: Session = Depends(get_db)):
    # 1. 대학 존재 여부 검증
    university = db.query(University).filter(University.id == univ_id).first()
    if not university:
        raise HTTPException(status_code=404, detail=f"University with ID {univ_id} not found")
    
    # 2. 해당 대학의 학과만 조회 (JOIN으로 확실히 보장)
    departments = db.query(Department).join(University).filter(
        Department.university_id == univ_id,
        Department.is_active == True  # 활성 학과만
    ).all()
    
    if not departments:
        raise HTTPException(status_code=404, detail=f"No active departments found for {university.name}")
    
    # 3. 응답 데이터 구성 (검증된 데이터만)
    result = []
    for dept in departments:
        exam_type = calculate_exam_type(university.name, dept.name, dept.division)
        
        result.append(DepartmentResponse(
            id=dept.id,
            name=dept.name,
            division=dept.division,
            exam_type=exam_type,
            university_name=university.name,
            full_identifier=f"{university.name}-{dept.name}"  # 고유 식별자
        ))
    
    return result

@app.post("/predict", response_model=PredictResponse)
def predict_admission(request: PredictRequest, db: Session = Depends(get_db)):
    # 1. 대학-학과 관계 검증 (이중 검증)
    dept = db.query(Department).join(University).filter(
        Department.id == request.dept_id,
        Department.university_id == request.university_id  # 추가 검증
    ).first()
    
    if not dept:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid department-university combination: dept_id={request.dept_id}, univ_id={request.university_id}"
        )
    
    # 2. 학과 활성 상태 검증
    if not dept.is_active:
        raise HTTPException(status_code=400, detail=f"Department {dept.name} is no longer active")
    
    # 3. 점수 유효성 검증
    exam_type = calculate_exam_type(dept.university.name, dept.name, dept.division)
    validate_scores(request, exam_type)
    
    # 나머지 예측 로직...
    
def validate_scores(request: PredictRequest, exam_type: str):
    """점수 유효성 검증"""
    if exam_type == "MATH_ONLY" and (not request.my_score_math or request.my_score_eng):
        raise HTTPException(status_code=400, detail="This department requires math score only")
    elif exam_type == "ENG_ONLY" and (not request.my_score_eng or request.my_score_math):
        raise HTTPException(status_code=400, detail="This department requires English score only")
    elif exam_type == "ENG_MATH" and (not request.my_score_eng or not request.my_score_math):
        raise HTTPException(status_code=400, detail="This department requires both English and math scores")

# 데이터 검증 유틸리티
def verify_department_integrity(db: Session):
    """데이터 무결성 검증 (관리자용)"""
    # 1. 고아 학과 검색
    orphan_depts = db.query(Department).outerjoin(University).filter(University.id.is_(None)).all()
    
    # 2. 중복 학과명 검색
    duplicate_depts = db.query(Department.university_id, Department.name, func.count(Department.id)).group_by(
        Department.university_id, Department.name
    ).having(func.count(Department.id) > 1).all()
    
    return {
        "orphan_departments": len(orphan_depts),
        "duplicate_departments": len(duplicate_depts),
        "issues": orphan_depts + [f"Duplicate: {d[1]} in univ_id {d[0]}" for d in duplicate_depts]
    }