#!/usr/bin/env python3
"""
DB 마이그레이션 및 로직 수정 검증 스크립트
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import University, AdmissionTrack, TrackType
from backend.services import calculate_admission_score

def verify_inha_data():
    """인하대 자연계열 데이터 무결성 검증"""
    print("=== 1. Inha University Natural Track Data Verification ===")
    
    db = SessionLocal()
    try:
        # 인하대 조회
        inha = db.query(University).filter(University.name == "인하대").first()
        if not inha:
            print("ERROR: Cannot find Inha University data.")
            return False
        
        # 자연계열 트랙 조회
        natural_track = db.query(AdmissionTrack).filter(
            AdmissionTrack.university_id == inha.id,
            AdmissionTrack.track_type.in_([TrackType.NATURAL_MAJOR, TrackType.NATURAL_GENERAL])
        ).first()
        
        if not natural_track:
            print("ERROR: Cannot find Inha University Natural track.")
            return False
        
        print(f"SUCCESS: Found Inha Natural track: {natural_track.track_type.value}")
        print(f"   - weight_ratio: {natural_track.weight_ratio}")
        print(f"   - max_score_eng: {natural_track.max_score_eng}")
        print(f"   - max_score_math: {natural_track.max_score_math}")
        print(f"   - total_max_score: {natural_track.total_max_score}")
        
        # weight_ratio 형식 검증
        if natural_track.weight_ratio and ":" in natural_track.weight_ratio:
            if not natural_track.weight_ratio.startswith("0"):
                print("SUCCESS: weight_ratio is in proper ratio format (not time format).")
                return True
            else:
                print("ERROR: weight_ratio is still in time format (02:50:00).")
                return False
        else:
            print("WARNING: Cannot verify weight_ratio format.")
            return False
            
    except Exception as e:
        print(f"ERROR during data verification: {e}")
        return False
    finally:
        db.close()

def test_calculation_logic():
    """점수 계산 로직 테스트"""
    print("\n=== 2. Score Calculation Logic Test ===")
    
    db = SessionLocal()
    try:
        # 인하대 자연계열 트랙 가져오기
        inha = db.query(University).filter(University.name == "인하대").first()
        if not inha:
            print("ERROR: Cannot find Inha University.")
            return False
        
        natural_track = db.query(AdmissionTrack).filter(
            AdmissionTrack.university_id == inha.id,
            AdmissionTrack.track_type.in_([TrackType.NATURAL_MAJOR, TrackType.NATURAL_GENERAL])
        ).first()
        
        if not natural_track:
            print("ERROR: Cannot find Natural track.")
            return False
        
        # 테스트 점수
        eng_score = 60
        math_score = 80
        
        print(f"Test scores: English {eng_score}, Math {math_score}")
        print(f"Track info:")
        print(f"  - max_score_eng: {natural_track.max_score_eng}")
        print(f"  - max_score_math: {natural_track.max_score_math}")
        print(f"  - total_max_score: {natural_track.total_max_score}")
        print(f"  - weight_ratio: {natural_track.weight_ratio}")
        
        # 점수 계산
        try:
            calculated_score = calculate_admission_score(natural_track, eng_score, math_score)
            print(f"SUCCESS: Calculated score: {calculated_score:.2f}")
            
            # 계산 로직 검증
            max_eng = natural_track.max_score_eng or 0
            max_math = natural_track.max_score_math or 0
            total_max = natural_track.total_max_score or 100
            
            if max_eng > 0 and max_math > 0:
                expected_formula = f"({eng_score}/{max_eng} * {max_eng} + {math_score}/{max_math} * {max_math}) * ({total_max}/{max_eng + max_math})"
                print(f"SUCCESS: Expected formula: {expected_formula}")
                
                # 수동 계산으로 검증
                eng_ratio = (eng_score / max_eng * max_eng) if max_eng > 0 else 0
                math_ratio = (math_score / max_math * max_math) if max_math > 0 else 0
                manual_calc = (eng_ratio + math_ratio) * (total_max / (max_eng + max_math))
                
                print(f"SUCCESS: Manual calculation result: {manual_calc:.2f}")
                
                if abs(calculated_score - manual_calc) < 0.01:
                    print("SUCCESS: Calculation logic works correctly.")
                    return True
                else:
                    print("ERROR: Calculation results do not match.")
                    return False
            else:
                print("WARNING: English or Math max score is 0.")
                return calculated_score > 0
                
        except Exception as e:
            print(f"ERROR during score calculation: {e}")
            return False
            
    except Exception as e:
        print(f"ERROR during test: {e}")
        return False
    finally:
        db.close()

def main():
    """메인 검증 함수"""
    print("DB Migration and Logic Fix Verification Started\n")
    
    # 1. 데이터 무결성 검증
    data_ok = verify_inha_data()
    
    # 2. 계산 로직 테스트
    calc_ok = test_calculation_logic()
    
    # 결과 요약
    print("\n=== Verification Summary ===")
    print(f"Data Integrity: {'PASS' if data_ok else 'FAIL'}")
    print(f"Calculation Logic: {'PASS' if calc_ok else 'FAIL'}")
    
    if data_ok and calc_ok:
        print("\nAll verifications completed successfully!")
        return True
    else:
        print("\nSome verifications found issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)