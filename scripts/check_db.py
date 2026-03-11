#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from backend.database import engine
from backend.models import University, AdmissionTrack

def check_database():
    """데이터베이스 현재 상태 확인"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # 대학 수 확인
        univ_count = session.query(University).count()
        track_count = session.query(AdmissionTrack).count()
        
        print(f"Universities: {univ_count}")
        print(f"Tracks: {track_count}")
        
        # 샘플 대학 조회
        sample_univs = session.query(University).limit(5).all()
        for univ in sample_univs:
            print(f"- {univ.name}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_database()