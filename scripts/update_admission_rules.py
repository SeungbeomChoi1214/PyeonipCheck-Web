from scripts.data_map import DATA_MAP
from backend.database import SessionLocal
from backend.models import University, AdmissionTrack, TrackType

def update_admission_rules():
    db = SessionLocal()
    updated_count = 0
    
    try:
        for univ_name, tracks in DATA_MAP.items():
            university = db.query(University).filter(University.name == univ_name).first()
            
            if not university:
                print(f"University {univ_name} not found in DB.")
                continue
            
            for track_name, data in tracks.items():
                track_type = TrackType.NATURAL_GENERAL if track_name == "Natural" else TrackType.HUMAN_GENERAL
                
                track = db.query(AdmissionTrack).filter(
                    AdmissionTrack.university_id == university.id,
                    AdmissionTrack.track_type == track_type
                ).first()
                
                if not track:
                    track = AdmissionTrack(
                        university_id=university.id,
                        track_type=track_type,
                        mu=70.0,
                        sigma=15.0
                    )
                    db.add(track)
                
                track.max_score_eng = data["max_eng"]
                track.max_score_math = data["max_math"]
                track.weight_ratio = data["ratio"]
                track.total_max_score = data["total"]
                
                updated_count += 1
        
        db.commit()
        print(f"Updated {updated_count} admission tracks successfully.")
        
    except Exception as e:
        db.rollback()
        print(f"Error updating admission rules: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_admission_rules()