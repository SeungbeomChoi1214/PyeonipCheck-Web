import numpy as np
from backend.database import SessionLocal
from backend.models import University, AdmissionTrack, StudentScore, TrackType

def split_total_score_by_ratio(total_score: float, weight_ratio: str, max_eng: int, max_math: int):
    """총점을 weight_ratio에 따라 영어/수학 점수로 분배"""
    weights = weight_ratio.split(":")
    w_eng, w_math = int(weights[0]), int(weights[1])
    
    if w_eng + w_math == 0:
        return 0, 0
    
    # 비율에 따른 점수 분배
    eng_portion = (w_eng / (w_eng + w_math)) * total_score
    math_portion = (w_math / (w_eng + w_math)) * total_score
    
    # 각 과목 만점 내로 제한
    eng_score = min(eng_portion, max_eng) if max_eng > 0 else 0
    math_score = min(math_portion, max_math) if max_math > 0 else 0
    
    return eng_score, math_score

def generate_simulation():
    db = SessionLocal()
    total_students = 0
    
    try:
        tracks = db.query(AdmissionTrack).join(University).all()
        
        for track in tracks:
            students = []
            
            for _ in range(300):
                # DB에서 이미 스케일링된 mu, sigma 사용
                total_score = np.random.normal(track.mu, track.sigma)
                
                # total_max_score 초과 방지
                total_score = min(total_score, track.total_max_score)
                total_score = max(0, total_score)  # 음수 방지
                
                # weight_ratio에 따라 영어/수학 점수 분배
                eng_score, math_score = split_total_score_by_ratio(
                    total_score, 
                    track.weight_ratio, 
                    track.max_score_eng or 0, 
                    track.max_score_math or 0
                )
                
                student = StudentScore(
                    track_id=track.id,
                    score_eng=eng_score,
                    score_math=math_score,
                    score_total=total_score
                )
                students.append(student)
            
            db.bulk_save_objects(students)
            total_students += 300
            print(f"Generated 300 students for {track.university.name} {track.track_type.value} (max: {track.total_max_score})")
        
        db.commit()
        print(f"✅ Generated {total_students} students successfully.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error generating simulation data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    generate_simulation()