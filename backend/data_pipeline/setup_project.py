import os

def create_project_files():
    # requirements.txt
    requirements_content = """fastapi
uvicorn
sqlalchemy
pydantic"""
    
    # database.py
    database_content = """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()"""
    
    # models.py
    models_content = """from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
class University(Base):
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    departments = relationship("Department", back_populates="university")
class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    univ_id = Column(Integer, ForeignKey("universities.id"))
    name = Column(String)
    university = relationship("University", back_populates="departments")
class ScoringRule(Base):
    __tablename__ = "scoring_rules"
    id = Column(Integer, primary_key=True, index=True)
    dept_id = Column(Integer, ForeignKey("departments.id"))
    stage1_eng_ratio = Column(Float, default=0.0)
    stage1_math_ratio = Column(Float, default=0.0)
    cut_off = Column(Float, default=0.0)"""
    
    # schemas.py
    schemas_content = """from pydantic import BaseModel, Field
class UserScoreInput(BaseModel):
    target_univ: str
    target_dept: str
    my_eng_score: float = Field(..., ge=0, le=100)
    my_math_score: float = Field(..., ge=0, le=100)
    my_gpa: float = Field(..., ge=0, le=4.5)
class PredictionOutput(BaseModel):
    university: str
    department: str
    calculated_score: float
    admission_probability: str
    comment: str"""
    
    # main.py
    main_content = """from fastapi import FastAPI, HTTPException
import models, schemas, database
models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
MOCK_RULES = {
    "경영학전공": {"eng": 1.0, "math": 0.0, "cut_off": 82.5},
    "컴퓨터공학전공": {"eng": 0.0, "math": 1.0, "cut_off": 78.0},
}
@app.post("/predict/gachon", response_model=schemas.PredictionOutput)
async def predict_gachon(input_data: schemas.UserScoreInput):
    rule = MOCK_RULES.get(input_data.target_dept)
    if not rule: raise HTTPException(status_code=404, detail="학과 데이터 없음")
    final_score = (input_data.my_eng_score * rule["eng"]) + (input_data.my_math_score * rule["math"])
    diff = final_score - rule["cut_off"]
    if diff >= 3: prob, msg = "안정", "합격 유력"
    elif diff >= 0: prob, msg = "적정", "추가 합격권"
    else: prob, msg = "불가", "상향 지원"
    return {"university": input_data.target_univ, "department": input_data.target_dept, "calculated_score": round(final_score, 2), "admission_probability": prob, "comment": msg}"""
    
    # 파일 생성
    files = {
        "requirements.txt": requirements_content,
        "database.py": database_content,
        "models.py": models_content,
        "schemas.py": schemas_content,
        "main.py": main_content
    }
    
    for filename, content in files.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename} 생성 완료")
    
    print("\n🎉 편입 합격 예측 서비스 백엔드 프로젝트 초기 세팅 완료!")

if __name__ == "__main__":
    create_project_files()