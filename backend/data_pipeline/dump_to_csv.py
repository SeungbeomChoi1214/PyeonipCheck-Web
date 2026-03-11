import re
import csv
import os

input_file = 'all_tables_raw.txt'  # 파일명 확인!
output_file = 'rough_data.csv'

def dump_everything():
    print("🚀 무식하게 긁어오기 시작...")
    
    if not os.path.exists(input_file):
        print("❌ 파일이 없어요! 경로를 확인하세요.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # csv 파일 열기 (utf-8-sig는 엑셀에서 한글 안 깨지게 함)
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 헤더: 대학명 | 원본 텍스트 | 숫자1 | 숫자2 | 숫자3 (혹시 몰라 넉넉히)
        writer.writerow(['University', 'Raw_Text', 'Num_1(Maybe_Gen)', 'Num_2(Maybe_Bach)', 'Num_3'])
        
        current_univ = "Unknown_Univ"
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # 1. 대학 이름 잡기 (단순 무식하게: '대학교' 포함되고 짧은 줄)
            if "대학교" in line and len(line) < 30 and not any(c.isdigit() for c in line):
                current_univ = line.replace("=", "").strip() # === 제거
                continue
            
            # 2. 숫자 잡기
            numbers = re.findall(r'\d+', line)
            
            # 숫자가 하나라도 있는 줄만 데이터로 인정하고 저장
            if numbers:
                # 엑셀에 [대학명, 원본텍스트, 숫자1, 숫자2, 숫자3...] 순서로 저장
                row = [current_univ, line] + numbers
                writer.writerow(row)

    print(f"✅ 끝! '{output_file}' 파일이 생성되었습니다.")
    print("이제 엑셀에서 열어서 눈으로 보고 정리하는 게 100배 빠릅니다.")

if __name__ == "__main__":
    dump_everything()