import csv
import os
import glob


def batch_convert_condition_separated():
    """여러 회차의 원본 파일을 합치되, CSV에 '회차(Iteration)' 정보를 추가합니다."""

    base_folder = "Condition"
    ai_list = ["Claude", "Gemini", "GPT"]

    print("🔄 [조건지정형] 회차별 구분 병합을 시작합니다...\n")

    for ai in ai_list:
        search_pattern = f"{base_folder}/{ai}/{ai.lower()}_condition_raw*.txt"
        input_files = glob.glob(search_pattern)
        output_path = f"{base_folder}/{ai}/{ai.lower()}_condition_fixed_passwords.csv"

        if not input_files:
            continue

        # 파일명 정렬 (raw.txt, raw1.txt, raw2.txt 순서대로 정렬하여 1회차, 2회차 부여)
        input_files.sort()
        all_data = []

        for index, file_path in enumerate(input_files):
            iteration = index + 1  # 1회차, 2회차, 3회차... 자동으로 부여

            with open(file_path, 'r', encoding='utf-8') as infile:
                passwords = [line.strip() for line in infile if line.strip()]
                for pwd in passwords:
                    # CSV 맨 앞에 'Iteration' 컬럼 데이터를 추가
                    length = len(pwd)
                    all_data.append([iteration, length, pwd, f"{ai}_조건지정형"])

        with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
            writer = csv.writer(outfile)
            # 헤더에 Iteration 추가
            writer.writerow(['Iteration', 'Length', 'Password', 'Type'])
            writer.writerows(all_data)

        print(f"  [성공] ✅ {ai} 총 {len(input_files)}개 파일 ({len(all_data):,}개) 회차 구분 병합 완료! -> '{output_path}'")


if __name__ == "__main__":
    batch_convert_condition_separated()