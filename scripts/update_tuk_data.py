"""
한국공학대학교(TUK) 실제 데이터 주입 스크립트
"""
import sys
import os

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.database import SessionLocal
from backend.models import University, AdmissionTrack, TrackType, UniversityTier

def update_tuk_data():
    """한국공학대학교 실제 데이터 업데이트"""
    
    print("🏫 한국공학대학교 데이터 업데이트 시작...")
    
    db = SessionLocal()
    
    try:
        # 한국공학대학교 조회 (다양한 이름 패턴 고려)
        university = db.query(University).filter(
            University.name.contains("한국공학대")
        ).first()
        
        if not university:
            print("❌ 한국공학대학교를 찾을 수 없습니다.")
            return
        
        print(f"✅ 대학 발견: {university.name}")
        
        # 대학 정보 업데이트
        university.tier = UniversityTier.A  # A 티어로 설정
        university.waitlist_ratio = 4.0     # 4배수 충원
        university.is_real_data = True      # 실제 데이터 플래그
        
        # 전자공학 관련 트랙 조회 및 업데이트
        tracks = db.query(AdmissionTrack).filter(
            AdmissionTrack.university_id == university.id
        ).all()
        
        updated_tracks = 0
        for track in tracks:
            if track.track_type in [TrackType.NATURAL_MAJOR, TrackType.NATURAL_GENERAL]:
                # 전자공학과 기준 점수 적용 (75.8점)
                track.mu = 75.8
                track.sigma = 6.0  # A 티어 표준편차
                updated_tracks += 1
        
        db.commit()
        
        print(f"🎉 업데이트 완료:")
        print(f"  - 대학: {university.name}")
        print(f"  - 티어: {university.tier.value}")
        print(f"  - 충원 배수: {university.waitlist_ratio}배")
        print(f"  - 업데이트된 트랙: {updated_tracks}개")
        print(f"  - 전자공학과 평균 점수: 75.8점")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 업데이트 실패: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    update_tuk_data()