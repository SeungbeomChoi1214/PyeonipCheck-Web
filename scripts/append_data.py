import pandas as pd
import io
import os

# ==========================================
# 👇 [여기] Amazon Q가 준 홍익대 데이터를 그대로 넣었습니다.
# ==========================================
new_data_text = """
university	department	division	stage1_eng	stage1_math	stage1_cut	has_stage2	stage2_keep	stage2_doc	stage2_int	final_cut
홍익대학교	전자·전기공학부	Natural	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	신소재공학전공	Natural	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	화학공학전공	Natural	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	컴퓨터공학과	Natural	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	산업·데이터공학과	Natural	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	기계·시스템디자인공학과	Natural	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	건설환경공학과	Natural	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	경영학전공	Humanities	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	영어영문학과	Humanities	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	독어독문학과	Humanities	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	불어불문학과	Humanities	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	국어국문학과	Humanities	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	법학부	Humanities	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	경제학전공	Humanities	0.5	0.5	0	TRUE	0.75	0.25	0	0
홍익대학교	전자전기융합공학과	Natural	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	소프트웨어융합학과	Natural	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	나노신소재학과	Natural	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	건축디자인전공	Natural	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	건축공학전공	Natural	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	기계정보공학과	Natural	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	조선해양공학과	Natural	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	바이오화학공학과	Natural	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	게임소프트웨어전공	Natural	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	회계학전공	Humanities	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	금융보험학전공	Humanities	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	글로벌경영전공	Humanities	0.0	0.0	0	TRUE	0.6	0.4	0	0
홍익대학교	광고홍보학부	Humanities	0.0	0.0	0	TRUE	0.6	0.4	0	0
"""
# ==========================================

FILENAME = "universities_data.xlsx"

def append_to_excel():
    # 1. 기존 엑셀 파일 불러오기
    if os.path.exists(FILENAME):
        try:
            df_existing = pd.read_excel(FILENAME)
            print(f"📂 기존 파일 로드 성공: {len(df_existing)}개 데이터")
        except Exception as e:
            print(f"❌ 기존 파일 읽기 실패: {e}")
            return
    else:
        print("⚠️ 기존 엑셀 파일이 없습니다. 새로 만듭니다.")
        df_existing = pd.DataFrame()

    # 2. 새로운 데이터(텍스트)를 데이터프레임으로 변환
    try:
        # delim_whitespace=True : 복사 과정에서 탭이 공백으로 바뀌어도 알아서 처리
        df_new = pd.read_csv(io.StringIO(new_data_text.strip()), delim_whitespace=True)
        print(f"✨ 홍익대 데이터 해석 성공: {len(df_new)}개 학과")
        
        # 3. 데이터 합치기 (기존 + 신규)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        
        # 중복 제거
        before_dedup = len(df_final)
        df_final.drop_duplicates(subset=['university', 'department'], inplace=True)
        dedup_count = before_dedup - len(df_final)
        
        if dedup_count > 0:
            print(f"🧹 중복 데이터 {dedup_count}개 제거됨")

        # 4. 저장하기
        df_final.to_excel(FILENAME, index=False)
        print(f"✅ 저장 완료! 총 데이터 개수: {len(df_final)}개")
        
    except Exception as e:
        print(f"❌ 데이터 변환 중 에러 발생: {e}")

if __name__ == "__main__":
    append_to_excel()