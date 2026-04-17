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

    # 퍼플렉시티 제거 완료
    target_files = [
        "BaseLine/baseline_condition_passwords.csv",
        "Condition/Claude/claude_condition_fixed_passwords.csv",
        "Condition/Gemini/gemini_condition_fixed_passwords.csv",
        "Condition/GPT/gpt_condition_fixed_passwords.csv"
    ]

    print("🛡️ [조건지정형 사전 대입 공격 방어율 검사 결과]")
    print("=" * 70)

    for file_path in target_files:
        if not os.path.exists(file_path):
            continue

        # 길이별로 데이터를 따로 모으기 위한 딕셔너리
        stats_by_length = {8: {'total': 0, 'leaked': 0, 'examples': []},
                           12: {'total': 0, 'leaked': 0, 'examples': []},
                           16: {'total': 0, 'leaked': 0, 'examples': []}}

        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                pwd = row['Password']
                length = int(row['Length'])

                if length not in stats_by_length:
                    stats_by_length[length] = {'total': 0, 'leaked': 0, 'examples': []}

                stats_by_length[length]['total'] += 1

                if pwd in rockyou_set:
                    stats_by_length[length]['leaked'] += 1
                    if len(stats_by_length[length]['examples']) < 3:
                        stats_by_length[length]['examples'].append(pwd)

        print(f"📁 {file_path.split('/')[-1]}")

        # 길이별 통계 출력
        for length in sorted(stats_by_length.keys()):
            stats = stats_by_length[length]
            total = stats['total']
            leaked = stats['leaked']

            if total > 0:
                leak_rate = (leaked / total) * 100
                safe_rate = 100 - leak_rate  # 방어율 계산

                print(f"   [길이: {length}자]")
                print(f"     - 총 검사 개수: {total}개")
                print(f"     - 유출 발견: {leaked}개 (취약도: {leak_rate:.2f}%)")
                print(f"     - 🛡️ 방어율: {safe_rate:.2f}%")
                if stats['examples']:
                    print(f"     - 유출 예시: {', '.join(stats['examples'])} ...")
        print("-" * 70)


if __name__ == "__main__":
    evaluate_dictionary_attack_condition()