"""
주요 대학 티어 시스템 일괄 업데이트 스크립트
"""
import sys
import os

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backend.database import SessionLocal
from backend.models import University, UniversityTier

def update_tiers():
    """주요 대학 티어 및 충원 배수 업데이트"""
    
    # 티어별 대학 매핑
    TIER_MAPPING = {
        'S': {
            'universities': ["한양대학교", "건국대학교", "동국대학교", "홍익대학교"],
            'waitlist_ratio': 2.5
        },
        'A': {
            'universities': ["가천대학교", "경기대학교", "세종대학교", "단국대학교", "아주대학교", "인하대학교"],
            'waitlist_ratio': 2.0
        },
        'B': {
            'universities': ["한국공학대학교", "수원대학교", "안양대학교"],
            'waitlist_ratio': 1.5
        }
    }
    
    print("🏫 주요 대학 티어 시스템 업데이트 시작...")
    
    db = SessionLocal()
    updated_count = 0
    
    try:
        for tier, config in TIER_MAPPING.items():
            print(f"\n📊 {tier} 티어 업데이트 중...")
            
            for univ_name in config['universities']:
                # 대학명 패턴 매칭 (부분 일치)
                university = db.query(University).filter(
                    University.name.contains(univ_name.replace("대학교", ""))
                ).first()
                
                if university:
                    # 티어 및 충원 배수 업데이트
                    university.tier = UniversityTier(tier)
                    university.waitlist_ratio = config['waitlist_ratio']
                    updated_count += 1
                    print(f"  ✅ {university.name}: {tier}티어, {config['waitlist_ratio']}배")
                else:
                    print(f"  ⚠️ {univ_name}: DB에서 찾을 수 없음")
        
        db.commit()
        print(f"\n🎉 업데이트 완료: {updated_count}개 대학")
        
        # 결과 확인
        print("\n📋 최종 티어 분포:")
        for tier in ['S', 'A', 'B', 'C']:
            count = db.query(University).filter(University.tier == UniversityTier(tier)).count()
            print(f"  {tier} 티어: {count}개 대학")
            
    except Exception as e:
        db.rollback()
        print(f"❌ 업데이트 실패: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    update_tiers()