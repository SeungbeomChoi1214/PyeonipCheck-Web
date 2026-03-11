#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from backend.database import engine
from backend.models import University, AdmissionTrack

# 대학별 가중치 매핑 데이터
UNIVERSITY_WEIGHT_MAP = {
    "인하대": {"max_eng": 100, "max_math": 100, "total": 130, "ratio": "80:50"},
    "한국공학대": {"max_eng": 100, "max_math": 100, "total": 200, "ratio": "50:50"},
    "서울과기대": {"max_eng": 100, "max_math": 100, "total": 150, "ratio": "60:40"},
    "국민대": {"max_eng": 100, "max_math": 100, "total": 120, "ratio": "70:30"},
    "단국대": {"max_eng": 100, "max_math": 100, "total": 110, "ratio": "80:20"}
}

def migrate_tracks():
    """AdmissionTrack 테이블에 가중치 데이터 적용"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        tracks = session.query(AdmissionTrack).join(University).all()
        updated_count = 0
        
        for track in tracks:
            univ_name = track.university.name
            
            for key, config in UNIVERSITY_WEIGHT_MAP.items():
                if key in univ_name:
                    track.max_score_eng = config["max_eng"]
                    track.max_score_math = config["max_math"]
                    track.total_max_score = config["total"]
                    track.weight_ratio = config["ratio"]
                    updated_count += 1
                    print(f"Updated: {univ_name} - {track.track_type.value}: {config['ratio']}")
                    break
        
        session.commit()
        print(f"Migration completed: {updated_count} tracks updated")
        
    except Exception as e:
        session.rollback()
        print(f"Migration failed: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    migrate_tracks()