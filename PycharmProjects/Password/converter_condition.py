import csv
import os

def batch_convert_condition():
    """Condition 폴더 안의 _condition_raw.txt 파일을 찾아 일괄 변환합니다."""

    # 목표 폴더는 오직 Condition!
    base_folder = "Condition"
    ai_list = ["Claude", "Gemini", "GPT", "Perplexity"]

    print("🔄 [조건지정형] 일괄 변환을 시작합니다...\n")

    for ai in ai_list:
        # 경로와 파일명에 모두 'condition'이 들어갑니다.
        input_path = f"{base_folder}/{ai}/{ai.lower()}_condition_raw.txt"
        output_path = f"{base_folder}/{ai}/{ai.lower()}_condition_fixed_passwords.csv"

        if not os.path.exists(input_path):
            print(f"  [건너뜀] ⚠️ '{input_path}' 파일을 찾을 수 없습니다.")
            continue

        with open(input_path, 'r', encoding='utf-8') as infile:
            passwords = [line.strip() for line in infile if line.strip()]

        with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Length', 'Password', 'Type'])

            for pwd in passwords:
                length = len(pwd)
                writer.writerow([length, pwd, f"{ai}_조건지정형"])

        print(f"  [성공] ✅ {ai} 조건지정형 변환 완료! -> '{output_path}'")

    print("\n🎉 변환 작업 완료! 이제 test_condition.py를 실행하세요!")


if __name__ == "__main__":
    batch_convert_condition()