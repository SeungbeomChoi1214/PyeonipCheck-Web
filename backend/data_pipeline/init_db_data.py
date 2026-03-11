import random
from sqlalchemy.orm import sessionmaker
from backend.database import engine, Base
from backend.models import University, AdmissionTrack, TrackType, StudentScore, ExamType

# 36개 대학 리스트
UNIVERSITIES = [
    "한양대", "서강대", "성균관대", "중앙대", "경희대", "한국외대", "건국대", "동국대",
    "홍익대", "숙실대", "국민대", "세종대", "광운대", "명지대", "단국대", "가천대",
    "인하대", "아주대", "경기대", "상명대", "용인대", "가톨릭대", "수원대", "강원대",
    "충남대", "충북대", "전남대", "전북대", "부산대", "경북대", "경남대", "인천대",
    "서울시립대", "부경대", "한국공학대", "숙명여대"
]

# 수학 100% 전형 대학 (자연계열)
MATH_ONLY_UNIVERSITIES = [
    "가천대", "한양대", "중앙대", "세종대", "가톨릭대", "단국대", "경희대", "한국공학대"
]

# Tier별 기준 데이터
TIER_DATA = {
    "S": {"MAJOR": {"mu": 88, "sigma": 5}, "GENERAL": {"mu": 80, "sigma": 7}},
    "A": {"MAJOR": {"mu": 78, "sigma": 6}, "GENERAL": {"mu": 70, "sigma": 8}},
    "B": {"MAJOR": {"mu": 68, "sigma": 8}, "GENERAL": {"mu": 60, "sigma": 10}}
}

# 대학별 Tier 분류 및 실제 지원자 수 (3개년 평균)
UNIVERSITY_DATA = {
    "한양대": {"tier": "S", "applicants": 2800}, "서강대": {"tier": "S", "applicants": 1500},
    "성균관대": {"tier": "S", "applicants": 2200}, "중앙대": {"tier": "S", "applicants": 2000},
    "경희대": {"tier": "S", "applicants": 1800}, "한국외대": {"tier": "A", "applicants": 1200},
    "건국대": {"tier": "A", "applicants": 1600}, "동국대": {"tier": "A", "applicants": 1400},
    "홍익대": {"tier": "A", "applicants": 1300}, "숙실대": {"tier": "A", "applicants": 1100},
    "국민대": {"tier": "A", "applicants": 1000}, "세종대": {"tier": "A", "applicants": 900},
    "광운대": {"tier": "A", "applicants": 800}, "명지대": {"tier": "A", "applicants": 750},
    "단국대": {"tier": "A", "applicants": 700}, "가천대": {"tier": "A", "applicants": 850},
    "인하대": {"tier": "A", "applicants": 950}, "아주대": {"tier": "A", "applicants": 900},
    "경기대": {"tier": "B", "applicants": 600}, "상명대": {"tier": "B", "applicants": 550},
    "용인대": {"tier": "B", "applicants": 400}, "가톨릭대": {"tier": "B", "applicants": 500},
    "수원대": {"tier": "B", "applicants": 450}, "강원대": {"tier": "B", "applicants": 650},
    "충남대": {"tier": "A", "applicants": 1100}, "충북대": {"tier": "B", "applicants": 600},
    "전남대": {"tier": "A", "applicants": 800}, "전북대": {"tier": "B", "applicants": 550},
    "부산대": {"tier": "A", "applicants": 1200}, "경북대": {"tier": "A", "applicants": 900},
    "경남대": {"tier": "B", "applicants": 500}, "인천대": {"tier": "B", "applicants": 600},
    "서울시립대": {"tier": "A", "applicants": 1400}, "부경대": {"tier": "B", "applicants": 550},
    "한국공학대": {"tier": "B", "applicants": 400}, "숙명여대": {"tier": "A", "applicants": 800}
}

def create_tracks_for_university(session, university_id: int, tier: str, univ_name: str):
    """대학에 4개 트랙 생성 및 각 트랙마다 500명 점수 생성"""
    tier_config = TIER_DATA[tier]
    
    tracks = [
        AdmissionTrack(
            university_id=university_id, track_type=TrackType.HUMAN_MAJOR,
            mu=tier_config["MAJOR"]["mu"], sigma=tier_config["MAJOR"]["sigma"], real_applicant_count=500
        ),
        AdmissionTrack(
            university_id=university_id, track_type=TrackType.HUMAN_GENERAL,
            mu=tier_config["GENERAL"]["mu"], sigma=tier_config["GENERAL"]["sigma"], real_applicant_count=500
        ),
        AdmissionTrack(
            university_id=university_id, track_type=TrackType.NATURAL_MAJOR,
            mu=tier_config["MAJOR"]["mu"], sigma=tier_config["MAJOR"]["sigma"], real_applicant_count=500
        ),
        AdmissionTrack(
            university_id=university_id, track_type=TrackType.NATURAL_GENERAL,
            mu=tier_config["GENERAL"]["mu"], sigma=tier_config["GENERAL"]["sigma"], real_applicant_count=500
        )
    ]
    
    for track in tracks:
        session.add(track)
        session.flush()
        
        track_name = track.track_type.value.replace('_', '-')
        print(f"[{univ_name}] {track_name}: 500명 점수 생성 중...")
        
        for _ in range(500):
            total_score = max(0, min(100, random.gauss(track.mu, track.sigma)))
            
            if 'NATURAL' in track.track_type.value:
                eng_score = total_score * 0.5
                math_score = total_score * 0.5
            else:
                eng_score = total_score
                math_score = 0
            
            student_score = StudentScore(
                track_id=track.id, score_eng=eng_score, score_math=math_score,
                score_total=total_score, is_virtual=True, is_spam=False
            )
            session.add(student_score)
        
        print(f"[{univ_name}] {track_name}: 500명 점수 생성 완료")

def init_database():
    """데이터베이스 초기화 및 4개 트랙 시스템 구축"""
    print("데이터베이스 초기화 중...")
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        for univ_name in UNIVERSITIES:
            univ_data = UNIVERSITY_DATA.get(univ_name, {"tier": "A", "applicants": 800})
            tier = univ_data["tier"]
            applicants = univ_data["applicants"]
            
            # exam_type 설정
            exam_type_natural = ExamType.MATH_ONLY if univ_name in MATH_ONLY_UNIVERSITIES else ExamType.ENG_MATH
            
            university = University(
                name=univ_name, tier_group=tier,
                exam_type_natural=exam_type_natural,
                exam_type_humanities=ExamType.ENG_ONLY,
                real_applicant_count=applicants
            )
            session.add(university)
            session.flush()
            
            create_tracks_for_university(session, university.id, tier, univ_name)
            
            exam_info = "수학100%" if exam_type_natural == ExamType.MATH_ONLY else "영어+수학"
            print(f"✅ {univ_name} (Tier {tier}, {exam_info}, {applicants}명) 완료")
        
        session.commit()
        print("\n🎉 데이터베이스 초기화 완료!")
        
        univ_count = session.query(University).count()
        track_count = session.query(AdmissionTrack).count()
        score_count = session.query(StudentScore).count()
        print(f"📊 최종 결과: 대학 {univ_count}, 트랙 {track_count}, 학생점수 {score_count}명")
        
    except Exception as e:
        session.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    init_database()