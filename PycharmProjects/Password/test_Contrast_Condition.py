import csv
import os


def evaluate_dictionary_attack_condition():
    rockyou_file = "rockyou.txt"

    print("⏳ RockYou 데이터셋 장전 중...")
    try:
        with open(rockyou_file, 'r', encoding='latin-1') as f:
            rockyou_set = set(line.strip() for line in f)
        print(f"✅ 총 {len(rockyou_set):,}개 장전 완료.\n")
    except FileNotFoundError:
        print(f"❌ '{rockyou_file}' 파일이 없습니다.")
        return

    target_files = [
        "BaseLine/baseline_condition_passwords.csv",
        "Condition/Claude/claude_condition_fixed_passwords.csv",
        "Condition/Gemini/gemini_condition_fixed_passwords.csv",
        "Condition/GPT/gpt_condition_fixed_passwords.csv",
        "Condition/Perplexity/perplexity_condition_fixed_passwords.csv"
    ]

    print("🛡️ [조건지정형 사전 대입 공격 방어율 검사 결과]")
    print("=" * 70)

    for file_path in target_files:
        if not os.path.exists(file_path):
            continue  # 파일이 없으면 메시지 없이 깔끔하게 다음 파일로 넘어감

        total_count = 0
        leaked_count = 0
        leaked_examples = []

        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                pwd = row['Password']
                total_count += 1

                if pwd in rockyou_set:
                    leaked_count += 1
                    if len(leaked_examples) < 3:
                        leaked_examples.append(pwd)

        if total_count > 0:
            leak_rate = (leaked_count / total_count) * 100
            safe_rate = 100 - leak_rate

            print(f"📁 {file_path.split('/')[-1]}")
            print(f"   - 총 검사 개수: {total_count}개")
            print(f"   - 유출 발견: {leaked_count}개 (취약도: {leak_rate:.2f}%)")
            print(f"   - 방어율: {safe_rate:.2f}%")
            if leaked_examples:
                print(f"   - 유출 예시: {', '.join(leaked_examples)} ...")
            print("-" * 70)


if __name__ == "__main__":
    evaluate_dictionary_attack_condition()