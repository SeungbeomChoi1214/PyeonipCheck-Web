import pdfplumber
import sys

# 사용법: python read_pdf.py "파일명.pdf"

def extract_tables_from_pdf(pdf_path):
    print(f"📄 Analyzing: {pdf_path} ...\n")
    
    with pdfplumber.open(pdf_path) as pdf:
        text_content = ""
        for i, page in enumerate(pdf.pages):
            # 1. 페이지에서 표 추출
            tables = page.extract_tables()
            
            if tables:
                print(f"--- [Page {i+1}] 표 발견 ---")
                for table in tables:
                    for row in table:
                        # None 데이터 처리 및 깔끔하게 합치기
                        clean_row = [str(cell).replace('\n', ' ') if cell else "" for cell in row]
                        row_text = " | ".join(clean_row)
                        print(row_text)
                        text_content += row_text + "\n"
                print("\n")
            else:
                # 표가 없으면 일반 텍스트 추출
                text = page.extract_text()
                if "전형" in text or "배점" in text: # 우리가 찾는 키워드
                     print(f"--- [Page {i+1}] 텍스트 (키워드 포함) ---")
                     print(text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python read_pdf.py [PDF파일명]")
    else:
        extract_tables_from_pdf(sys.argv[1])