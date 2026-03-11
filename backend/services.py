from backend.models import TrackType, AdmissionTrack, University
from sqlalchemy.orm import Session

# =========================================================
# 🚨 [Phase 1] 대학 티어 및 학과 가중치 정의
# =========================================================

UNIVERSITY_TIER_MAP = {
    # [Tier 1] 최상위권
    "성균관대": 1.25, "한양대": 1.25, "서강대": 1.25, 
    "이화여대": 1.2, "중앙대": 1.2, "경희대": 1.2, "한국외대": 1.15, "서울시립대": 1.15,
    # [Tier 2] 상위권
    "건국대": 1.15, "동국대": 1.15, "홍익대": 1.15,
    "국민대": 1.05, "숭실대": 1.05, "세종대": 1.05, "단국대": 1.0, 
    "아주대": 1.1, "인하대": 1.1, "서울과기대": 1.05, "항공대": 1.05,
    # [Tier 3] 인서울/수도권 주요
    "가천대": 0.95, "경기대": 0.95, "명지대": 0.95, "상명대": 0.95, 
    "가톨릭대": 0.95, "광운대": 1.0, "서울여대": 0.95, "동덕여대": 0.95, 
    "덕성여대": 0.95, "성신여대": 0.95,
    # [Tier 4] 기타
    "한국공학대": 0.9, "수원대": 0.85, "서경대": 0.9, "삼육대": 0.9, 
    "한성대": 0.9, "인천대": 0.95
}

CLUSTER_WEIGHT_MAP = {
    # 자연계열
    "HIGH_TECH": 1.08, "MAJOR_ENG": 1.03, "PURE_SCI": 0.98, "ETC_NAT": 0.95,
    # 인문계열
    "BIZ_TOP": 1.08, "SOC_SCI": 1.02, "HUM_LIT": 0.98, "ETC_HUM": 0.95,
    # 기본
    "DEFAULT": 1.0
}

# =========================================================
# 3. API 응답 생성 (Service Wrapper) - 최종 수정판
# =========================================================

def analyze_user_admission(db: Session, univ_id: int, category_code: str, eng: float, math: float):
    # 1. 대학 정보 조회
    univ = db.query(University).filter(University.id == univ_id).first()
    if not univ:
        return {"error": "University not found"}
    
    # ---------------------------------------------------------
    # A. 동적 컷라인 생성 (Dynamic Cutline)
    # ---------------------------------------------------------
    tier_multiplier = 0.9
    for key, value in UNIVERSITY_TIER_MAP.items():
        if key in univ.name:
            tier_multiplier = value
            break
            
    cluster_weight = CLUSTER_WEIGHT_MAP.get(category_code, 1.0)
    
    # 예상 합격 컷 계산
    calculated_cutline = 70.0 * tier_multiplier * cluster_weight
    final_cutline = min(round(calculated_cutline, 1), 98.0)
    
    # ---------------------------------------------------------
    # B. 내 점수 계산 및 전형 판단
    # ---------------------------------------------------------
    # 자연계열 판단 (수학 점수가 있거나, 카테고리가 자연계열)
    is_natural = math > 0 or category_code in ["HIGH_TECH", "MAJOR_ENG", "PURE_SCI", "ETC_NAT"]
    
    # 예외 대학 (수학 100%)
    MATH_ONLY_UNIVS = ["한양대", "단국대", "세종대", "가천대", "한국공학대"]
    is_math_only = any(u in univ.name for u in MATH_ONLY_UNIVS) and is_natural

    # 점수 환산
    if is_natural:
        if is_math_only:
            my_score = math # 수학 100%
        else:
            my_score = (eng * 0.5) + (math * 0.5) # 영수 50:50
    else:
        my_score = eng # 인문계 영어 100%
        
    my_score = min(my_score, 100.0)

    # ---------------------------------------------------------
    # C. 전략 분석 및 결과 생성
    # ---------------------------------------------------------
    gap = my_score - final_cutline
    
    if gap >= 0.1:
        status = "안정 (Safe)"
        message = "🟢 합격권입니다! 대학별 고사 실전 연습에 집중하세요."
        color = "green"
    elif -5.0 <= gap < 0.1:
        status = "적정 (Proper)"
        message = "🟡 추가합격권입니다. 한 문제 차이입니다. 끝까지 포기하지 마세요."
        color = "#FFC107"
    elif -15.0 <= gap < -5.0:
        status = "소신 (Challenge)"
        message = "🟠 상향 지원입니다. 남은 기간 취약 파트를 집중 공략해야 합니다."
        color = "orange"
    else:
        status = "위험 (Danger)"
        message = "🔴 합격 확률이 낮습니다. 안정적인 대학을 함께 고려해보세요."
        color = "red"

    # [중요] 차트 표시용 메타데이터 생성
    if is_natural:
        if is_math_only:
            disp_max_eng = 0
            disp_max_math = 100
            disp_ratio = "0:100"
        else:
            disp_max_eng = 100
            disp_max_math = 100
            disp_ratio = "50:50"
    else:
        # 인문계
        disp_max_eng = 100
        disp_max_math = 0
        disp_ratio = "100:0"

    # ... (위쪽 로직 유지) ...

    # [추가] 평균 점수 계산 (컷라인보다 10~15점 낮게 설정하여 현실감 부여)
    average_score = final_cutline - 12.0
    
    # 점수가 너무 낮아지지 않게 최소 40점 방어
    average_score = max(average_score, 40.0)

    # 4. 최종 리턴
    return {
        "univ_name": univ.name,
        "dept_category": category_code,
        "my_score": round(my_score, 2),
        "cutline": final_cutline,
        "average_score": round(average_score, 1), # ★ 새로 추가된 키!
        "gap": round(gap, 2),
        "status": status,
        "message": message,
        "ui_color": color,
        
        "max_score_eng": disp_max_eng,
        "max_score_math": disp_max_math,
        "weight_ratio": disp_ratio
    }