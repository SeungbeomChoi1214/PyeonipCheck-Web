# 개선된 데이터 모델 (models_v2.py)

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class University(Base):
    __tablename__ = "universities"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True)  # 대학 고유 코드 (예: KU001)
    name = Column(String(100), unique=True, index=True)
    official_name = Column(String(200))  # 정식 명칭
    
    # 메타데이터
    established_year = Column(Integer)
    region = Column(String(50))
    tier_group = Column(String(10))
    
    # 관계
    departments = relationship("Department", back_populates="university")
    
    def __repr__(self):
        return f"<University(code={self.code}, name={self.name})>"

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    
    # 복합 식별자
    code = Column(String(20), nullable=False)  # 학과 코드 (예: CSE, BUS)
    name = Column(String(100), nullable=False)
    official_name = Column(String(200))  # 정식 학과명
    
    # 비즈니스 속성
    division = Column(String(20), nullable=False)  # Humanities/Natural
    college = Column(String(100))  # 소속 단과대학
    
    # 메타데이터
    established_year = Column(Integer)
    is_active = Column(Boolean, default=True)
    last_verified = Column(DateTime, default=func.now())
    
    # 복합 유니크 제약 (대학 내 학과 코드 중복 방지)
    __table_args__ = (
        UniqueConstraint('university_id', 'code', name='uq_univ_dept_code'),
        UniqueConstraint('university_id', 'name', name='uq_univ_dept_name'),
    )
    
    # 관계
    university = relationship("University", back_populates="departments")
    student_scores = relationship("StudentScore", back_populates="department")
    
    @property
    def full_code(self):
        """대학코드-학과코드 조합"""
        return f"{self.university.code}-{self.code}"
    
    def __repr__(self):
        return f"<Department(full_code={self.full_code}, name={self.name})>"

class StudentScore(Base):
    __tablename__ = "student_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    
    # 점수 정보
    score_eng = Column(Float)
    score_math = Column(Float)
    score_total = Column(Float, nullable=False)
    
    # 메타데이터
    is_virtual = Column(Boolean, default=False, index=True)
    is_spam = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=func.now())
    
    # 관계
    department = relationship("Department", back_populates="student_scores")
    
    def __repr__(self):
        return f"<StudentScore(dept={self.department.full_code}, total={self.score_total})>"