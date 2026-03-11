import os
import sys

# 모듈 경로 문제 방지
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import engine, SessionLocal, Base
from backend.models import University, AdmissionTrack, TrackType
from scripts.data_map import DATA_MAP, generate_weight_ratio

# 티어별 기본 mu/sigma 값 (100점 만점 기준)
BASE_TIER_CONFIG = {
    "S": {"mu": 85, "sigma": 12},
    "A": {"mu": 78, "sigma": 15}, 
    "B": {"mu": 70, "sigma": 18},
    "C": {"mu": 62, "sigma": 20}
}

# 대학별 티어 매핑
UNIVERSITY_TIERS = {
    "연세대": "S", "고려대": "S", "서강대": "S",
    "성균관대": "A", "한양대": "A", "중앙대": "A", "경희대": "A", "이화여대": "A",
    "건국대": "B", "동국대": "B", "홍익대": "B", "숭실대": "B", "인하대": "B",
    "가천대": "C", "명지대": "C", "단국대": "C"
}

def get_scaled_mu_sigma(univ_name: str, total_max_score: int):
    """대학 티어와 총점에 따라 스케일링된 mu, sigma 반환"""
    tier = UNIVERSITY_TIERS.get(univ_name, "B")  # 기본값 B티어
    base_config = BASE_TIER_CONFIG[tier]
    
    # 스케일링 비율 계산
    ratio = total_max_score / 100.0
    
    scaled_mu = base_config["mu"] * ratio
    scaled_sigma = base_config["sigma"] * ratio
    
    return scaled_mu, scaled_sigma

def validate_score_consistency(max_eng: int, max_math: int, total: int) -> bool:
    """영어+수학 점수가 총점과 일치하는지 검증"""
    return (max_eng + max_math) == total

def reset_and_init_db():
    # 1. Delete Old DB
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'university.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Old database deleted.")
    
    # 2. Create New Tables
    Base.metadata.create_all(bind=engine)
    print("✨ New tables created (Schema updated).")
    
    # 3. Inject Data
    db = SessionLocal()
    univ_count = 0
    track_count = 0
    
    try:
        for univ_name in DATA_MAP.keys():
            # Create University
            university = University(name=univ_name)
            db.add(university)
            db.flush()
            univ_count += 1
            
            # Create Natural Track
            natural_data = DATA_MAP[univ_name]["Natural"]
            
            # 점수 일관성 검증
            if not validate_score_consistency(natural_data["max_eng"], natural_data["max_math"], natural_data["total"]):
                print(f"⚠️ Score inconsistency for {univ_name} Natural: {natural_data["max_eng"]}+{natural_data["max_math"]} != {natural_data["total"]}")
            
            # 스케일링된 mu, sigma 계산
            scaled_mu, scaled_sigma = get_scaled_mu_sigma(univ_name, natural_data["total"])
            
            natural_track = AdmissionTrack(
                university_id=university.id,
                track_type=TrackType.NATURAL_GENERAL,
                mu=scaled_mu,
                sigma=scaled_sigma,
                max_score_eng=natural_data["max_eng"],
                max_score_math=natural_data["max_math"],
                weight_ratio=generate_weight_ratio(natural_data["max_eng"], natural_data["max_math"]),
                total_max_score=natural_data["total"]
            )
            db.add(natural_track)
            track_count += 1
            
            # Create Humanities Track
            humanities_data = DATA_MAP[univ_name]["Humanities"]
            
            # 점수 일관성 검증
            if not validate_score_consistency(humanities_data["max_eng"], humanities_data["max_math"], humanities_data["total"]):
                print(f"⚠️ Score inconsistency for {univ_name} Humanities: {humanities_data["max_eng"]}+{humanities_data["max_math"]} != {humanities_data["total"]}")
            
            # 스케일링된 mu, sigma 계산
            scaled_mu, scaled_sigma = get_scaled_mu_sigma(univ_name, humanities_data["total"])
            
            humanities_track = AdmissionTrack(
                university_id=university.id,
                track_type=TrackType.HUMAN_GENERAL,
                mu=scaled_mu,
                sigma=scaled_sigma,
                max_score_eng=humanities_data["max_eng"],
                max_score_math=humanities_data["max_math"],
                weight_ratio=generate_weight_ratio(humanities_data["max_eng"], humanities_data["max_math"]),
                total_max_score=humanities_data["total"]
            )
            db.add(humanities_track)
            track_count += 1
        
        db.commit()
        
        # 4. Verify
        print(f"✅ Inserted {univ_count} universities and {track_count} tracks successfully.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error during data injection: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_and_init_db()