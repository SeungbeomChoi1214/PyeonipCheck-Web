import pandas as pd

# 1. 엑셀에 들어갈 헤더(제목)와 예시 데이터 정의
data = {
    "university": ["가천대학교", "한양대학교", "건국대학교(예시)"],
    "department": ["경영학전공", "경영학부", "컴퓨터공학부"],
    "division": ["Humanities", "Humanities", "Natural"],
    
    # 1단계 비율 (0.0 ~ 1.0)
    "stage1_eng": [1.0, 1.0, 0.0],
    "stage1_math": [0.0, 0.0, 1.0],
    "stage1_cut": [0, 80, 75], # 1단계 컷트라인
    
    # 2단계 여부 (True/False)
    # Python에서는 True/False로 쓰면 엑셀에서도 잘 인식합니다.
    "has_stage2": [False, True, True],
    
    # 2단계 반영 비율 (총합이 1.0이 되도록)
    "stage2_keep": [0.0, 0.7, 0.6], # 1단계 성적 반영비
    "stage2_doc": [0.0, 0.3, 0.4],  # 서류 비율
    "stage2_int": [0.0, 0.0, 0.0],  # 면접 비율
    
    # 최종 합격 컷
    "final_cut": [70, 88, 85]
}

# 2. 데이터프레임 만들기 (직관적으로 바로 생성)
df = pd.DataFrame(data)

# 3. 엑셀 파일로 저장
filename = "universities_data.xlsx"
# engine='openpyxl'을 명시해주는 것이 안전합니다.
df.to_excel(filename, index=False, engine='openpyxl')

print(f"✅ '{filename}' 파일이 생성되었습니다!")