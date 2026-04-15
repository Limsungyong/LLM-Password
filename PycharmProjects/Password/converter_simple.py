import csv
import os


def batch_convert(prompt_type="단순형"):
    """Simple 폴더 안에 있는 4개 AI의 _simple_raw.txt 파일을 찾아 일괄 변환합니다."""

    # 우리가 데이터를 모아둔 가장 큰 폴더 이름
    base_folder = "Simple"
    ai_list = ["Claude", "Gemini", "GPT", "Perplexity"]

    print(f"🔄 '{prompt_type}' 일괄 변환을 시작합니다...\n")

    for ai in ai_list:
        # 💡 수정된 부분 1: 앞에 'Simple/' 경로 추가
        # 💡 수정된 부분 2: 파일 이름에 '_simple' 추가
        input_path = f"{base_folder}/{ai}/{ai.lower()}_simple_raw.txt"
        output_path = f"{base_folder}/{ai}/{ai.lower()}_simple_fixed_passwords.csv"

        # 파일이 존재하는지 확인
        if not os.path.exists(input_path):
            print(f"  [건너뜀] ⚠️ '{input_path}' 파일을 찾을 수 없습니다.")
            continue

        # 텍스트 파일 읽어오기
        with open(input_path, 'r', encoding='utf-8') as infile:
            passwords = [line.strip() for line in infile if line.strip()]

        # CSV 양식으로 저장하기
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Length', 'Password', 'Type'])

            for pwd in passwords:
                length = len(pwd)
                writer.writerow([length, pwd, f"{ai}_{prompt_type}"])

        print(f"  [성공] {ai} 데이터 변환 완료! -> '{output_path}'")

    print("\n 모든 변환 작업이 끝났습니다. 이제 test.py를 실행하세요!")


if __name__ == "__main__":
    batch_convert("단순형")