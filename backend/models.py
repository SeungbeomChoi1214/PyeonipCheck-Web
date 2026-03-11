from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base
import enum

class TrackType(enum.Enum):
    HUMAN_MAJOR = "HUMAN_MAJOR"
    HUMAN_GENERAL = "HUMAN_GENERAL"
    NATURAL_MAJOR = "NATURAL_MAJOR"
    NATURAL_GENERAL = "NATURAL_GENERAL"

class ExamType(enum.Enum):
    MATH_ONLY = "MATH_ONLY"
    ENG_ONLY = "ENG_ONLY"
    ENG_MATH = "ENG_MATH"

class UniversityTier(enum.Enum):
    S = "S"
    A = "A"
    B = "B"
    C = "C"

class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    tier_group = Column(String, default="A")
    tier = Column(Enum(UniversityTier), default=UniversityTier.B)
    waitlist_ratio = Column(Float, default=1.5)
    is_real_data = Column(Boolean, default=False)  # 실제 데이터 여부
    exam_type_natural = Column(Enum(ExamType), default=ExamType.ENG_MATH)
    exam_type_humanities = Column(Enum(ExamType), default=ExamType.ENG_ONLY)
    real_applicant_count = Column(Integer, default=1200)  # 3개년 평균 지원자 수
    
    # 관계 설정
    tracks = relationship("AdmissionTrack", back_populates="university", cascade="all, delete-orphan")

class AdmissionTrack(Base):
    __tablename__ = "admission_tracks"

    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    track_type = Column(Enum(TrackType), nullable=False)
    
    # 시뮬레이션용 통계 데이터
    mu = Column(Float, nullable=False)  # 평균
    sigma = Column(Float, nullable=False)  # 표준편차
    real_applicant_count = Column(Integer, default=500)  # 실제 지원자 수 추정치
    
    # 복합 과목 점수 산출 로직
    max_score_eng = Column(Integer, nullable=True, default=100)  # 영어 만점
    max_score_math = Column(Integer, nullable=True, default=100)  # 수학 만점
    total_max_score = Column(Integer, nullable=True, default=100)  # 총 만점
    weight_ratio = Column(String, nullable=True, default="100:0")  # 가중치 비율 (영어:수학)
    
    # 관계 설정
    university = relationship("University", back_populates="tracks")
    student_scores = relationship("StudentScore", back_populates="track", cascade="all, delete-orphan")

class StudentScore(Base):
    __tablename__ = "student_scores"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("admission_tracks.id"), nullable=False)
    
    # 점수 정보
    score_eng = Column(Float)
    score_math = Column(Float)
    score_total = Column(Float, nullable=False)
    
    # 허수 방어
    is_virtual = Column(Boolean, default=False, index=True)
    is_spam = Column(Boolean, default=False, index=True)
    
    # 메타 정보
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계 설정
    track = relationship("AdmissionTrack", back_populates="student_scores")