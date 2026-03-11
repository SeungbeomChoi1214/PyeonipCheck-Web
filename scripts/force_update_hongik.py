import pandas as pd
import io
import os

FILENAME = "universities_data.xlsx"

# 홍익대학교 데이터 (누락되었을 경우를 대비해 다시 준비)
hongik_data_str = """
university  department  division    stage1_eng  stage1_math stage1_cut  has_stage2  stage2_keep stage2_doc  stage2_int  final_cut
홍익대학교  전자·전기공학부 Natural 0.5 0.5 0   TRUE    0.75    0.25    0   0
홍익대학교  신소재공학전공   Natural 0.5 0.5 0   TRUE    0.75    0.25    0   0
홍익대학교  화학공학전공    Natural 0.5 0.5 0   TRUE    0.75    0.25    0   0
홍익대학교  컴퓨터공학과    Natural 0.5 0.5 0   TRUE    0.75    0.25    0   0
홍익대학교  산업·데이터공학과 Natural 0.5 0.5 0   TRUE    0.75    0.25    0   0
홍익대학교  기계·시스템디자인공학과    Natural 0.5 0.5 0   TRUE    0.75    0.25    0   0
홍익대학교  건설환경공학과   Natural 0.5 0.5 0   TRUE    0.75    0.25    0   0
홍익대학교  경영학전공 Humanities  1.0 0.0 0   TRUE    0.75    0.25    0   0
홍익대학교  영어영문학과    Humanities  1.0 0.0 0   TRUE    0.75    0.25    0   0
홍익대학교  독어독문학과    Humanities  1.0 0.0 0   TRUE    0.75    0.25    0   0
홍익대학교  불어불문학과    Humanities  1.0 0.0 0   TRUE    0.75    0.25    0   0
홍익대학교  국어국문학과    Humanities  1.0 0.0 0   TRUE    0.75    0.25    0   0
홍익대학교  법학부 Humanities  1.0 0.0 0   TRUE    0.75    0.25    0   0
홍익대학교  경제학전공 Humanities  1.0 0.0 0   TRUE    0.75    0.25    0   0
홍익대학교  전자전기융합공학과  Natural 0.5 0.5 0   TRUE    0.6 0.4 0   0
홍익대학교  소프트웨어융합학과  Natural 0.5 0.5 0   TRUE    0.6 0.4 0   0
홍익대학교  나노신소재학과   Natural 0.5 0.5 0   TRUE    0.6 0.4 0   0
홍익대학교  건축디자인전공   Natural 0.5 0.5 0   TRUE    0.6 0.4 0   0
홍익대학교  건축공학전공    Natural 0.5 0.5 0   TRUE    0.6 0.4 0   0
홍익대학교  기계정보공학과   Natural 0.5 0.5 0   TRUE    0.6 0.4 0   0
홍익대학교  조선해양공학과   Natural 0.5 0.5 0   TRUE    0.6 0.4 0   0
홍익대학교  바이오화학공학과  Natural 0.5 0.5 0   TRUE    0.6 0.4 0   0
홍익대학교  게임소프트웨어전공  Natural 0.5 0.5 0   TRUE    0.6 0.4 0   0
홍익대학교  회계학전공 Humanities  1.0 0.0 0   TRUE    0.6 0.4 0   0
홍익대학교  금융보험학전공   Humanities  1.0 0.0 0   TRUE    0.6 0.4 0   0
홍익대학교  글로벌경영전공   Humanities  1.0 0.0 0   TRUE    0.6 0.4 0   0
홍익대학교  광고홍보학부    Humanities  1.0 0.0 0   TRUE    0.6 0.4 0   0
"""

def update_hongik():
    # 1. 파일 열기
    if os.path.exists(FILENAME):
        df = pd.read_excel(FILENAME)
        print(f"📂 현재 파일 데이터 개수: {len(df)}개")
    else:
        print("❌ 파일이 없습니다. 새로 생성합니다.")
        df = pd.DataFrame()

    # 2. 홍익대 데이터가 이미 있는지 확인
    hongik_exists = df['university'].str.contains('홍익대학교').any()

    if not hongik_exists:
        print("⚠️ 홍익대 데이터가 없어서 새로 추가합니다...")
        df_hongik = pd.read_csv(io.StringIO(hongik_data_str.strip()), delim_whitespace=True)
        df = pd.concat([df, df_hongik], ignore_index=True)
    else:
        print("ℹ️ 홍익대 데이터가 이미 존재합니다. (업데이트만 진행)")

    # 3. [자동 수정] 홍익대 인문계열은 영어 100% (1.0), 수학 0% (0.0)로 강제 설정
    # 조건: 대학='홍익대학교' AND 계열='Humanities'
    mask_human = (df['university'] == '홍익대학교') & (df['division'] == 'Humanities')
    df.loc[mask_human, 'stage1_eng'] = 1.0
    df.loc[mask_human, 'stage1_math'] = 0.0

    # 4. [자동 수정] 홍익대 자연계열은 영어 50% (0.5), 수학 50% (0.5)로 강제 설정
    mask_natural = (df['university'] == '홍익대학교') & (df['division'] == 'Natural')
    df.loc[mask_natural, 'stage1_eng'] = 0.5
    df.loc[mask_natural, 'stage1_math'] = 0.5
    
    # 5. 중복 제거 (혹시 모르니)
    df.drop_duplicates(subset=['university', 'department'], inplace=True)

    # 6. 저장 및 검증
    df.to_excel(FILENAME, index=False)
    
    print("-" * 30)
    print(f"✅ 수정 완료! 총 데이터 개수: {len(df)}개")
    print("🔍 [검증] 마지막 3개 데이터:")
    print(df.tail(3)[['university', 'department', 'stage1_eng', 'stage1_math']])
    print("-" * 30)

if __name__ == "__main__":
    update_hongik()