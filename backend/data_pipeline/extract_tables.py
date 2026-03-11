import pdfplumber
import os

PDF_FOLDER = "pdfs"
OUTPUT_FILE = "all_tables_raw.txt"

def extract_all_tables():
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
    print(f"🔍 총 {len(pdf_files)}개 대학의 표 데이터를 '강력 세척'하여 추출합니다...\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
        for pdf_file in pdf_files:
            path = os.path.join(PDF_FOLDER, pdf_file)
            print(f"Processing: {pdf_file}...")
            
            f_out.write(f"\n{'='*50}\n")
            f_out.write(f"[[ 대학명: {pdf_file} ]]\n")
            f_out.write(f"{'='*50}\n")
            
            try:
                with pdfplumber.open(path) as pdf:
                    for i, page in enumerate(pdf.pages):
                        tables = page.extract_tables()
                        if tables:
                            f_out.write(f"\n--- Page {i+1} ---\n")
                            for table in tables:
                                for row in table:
                                    # 💡 [핵심] isprintable() : 출력 가능한 '진짜 글자'만 남기고 기계어는 다 버림
                                    clean_row = []
                                    for cell in row:
                                        if cell:
                                            # 줄바꿈은 공백으로, 나머지 이상한 문자는 삭제
                                            cleaned_text = "".join(ch for ch in str(cell) if ch.isprintable())
                                            clean_row.append(cleaned_text)
                                        else:
                                            clean_row.append("")
                                            
                                    row_str = " | ".join(clean_row)
                                    f_out.write(row_str + "\n")
                                f_out.write("-" * 20 + "\n")
            except Exception as e:
                print(f"⚠️ 에러 ({pdf_file}): {e}")

    print(f"\n✅ 강력 세척 완료! 이제 '{OUTPUT_FILE}' 파일이 잘 열릴 겁니다.")

if __name__ == "__main__":
    extract_all_tables()