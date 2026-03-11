import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database import get_db, engine
import backend.models as models
import backend.services as services

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionInput(BaseModel):
    university_name: str
    dept_name: str
    user_division: str
    category_code: str
    score_eng: float
    score_math: float

@app.get("/universities")
def get_universities(db: Session = Depends(get_db)):
    """대학 목록과 전형 정보 반환 (안전 모드 적용)"""
    univs = db.query(models.University).all()
    result = []
    
    for u in univs:
        # 기본값 설정 (DB에 정보가 없어도 이 값이 나감)
        natural_info = {"subjects": "English + Math", "has_eng": True, "has_math": True}
        humanities_info = {"subjects": "English Only", "has_eng": True, "has_math": False}
        
        # DB에서 트랙 정보 조회 시도
        tracks = db.query(models.AdmissionTrack).filter(models.AdmissionTrack.university_id == u.id).all()
        
        # 트랙 정보가 있으면 업데이트 (없으면 위 기본값 유지 -> 에러 방지)
        for track in tracks:
            max_eng = track.max_score_eng or 0
            max_math = track.max_score_math or 0
            
            if "NATURAL" in track.track_type.value.upper():
                if max_eng == 0 and max_math > 0:
                    natural_info = {"subjects": "Math Only", "has_eng": False, "has_math": True}
                elif max_eng > 0 and max_math == 0:
                    natural_info = {"subjects": "English Only", "has_eng": True, "has_math": False}
            
            elif "HUMAN" in track.track_type.value.upper():
                if max_eng == 0 and max_math > 0:
                    humanities_info = {"subjects": "Math Only", "has_eng": False, "has_math": True}
                elif max_eng > 0 and max_math > 0:
                    humanities_info = {"subjects": "English + Math", "has_eng": True, "has_math": True}
        
        # 특정 대학 예외 처리
        if "경기대" in u.name:
            # 경기대는 자연계열도 영어+수학 전형
            natural_info = {"subjects": "English + Math", "has_eng": True, "has_math": True}
        
        result.append({
            "id": u.id,
            "name": u.name,
            "exam_info": {
                "Natural": natural_info,
                "Humanities": humanities_info
            }
        })
    
    return result

@app.post("/predict")
def predict_admission(input_data: PredictionInput, db: Session = Depends(get_db)):
    univ = db.query(models.University).filter(models.University.name.like(f"%{input_data.university_name}%")).first()
    
    if not univ:
        # DB에 없는 대학은 가상 ID 처리
        univ_id = 1 
    else:
        univ_id = univ.id

    try:
        result = services.analyze_user_admission(
            db=db,
            univ_id=univ_id,
            category_code=input_data.category_code,
            eng=input_data.score_eng,
            math=input_data.score_math
        )
        result["dept_name"] = input_data.dept_name
        return result

    except Exception as e:
        print(f"Prediction Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

        # === [이 부분을 main.py 에 추가하세요] ===

@app.get("/departments")
def get_departments(univ_id: int, db: Session = Depends(get_db)):
    """특정 대학(univ_id)의 학과 목록을 반환"""
    # DB에서 해당 대학의 학과들을 찾음
    depts = db.query(models.Department).filter(models.Department.university_id == univ_id).all()
    
    result = []
    for d in depts:
        result.append({
            "id": d.id,
            "name": d.name,
            "category": d.category, # 인문/자연 구분 코드
            "quota": d.quota_general if d.quota_general else 0 # 모집 인원
        })
    return result