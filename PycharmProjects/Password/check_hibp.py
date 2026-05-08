import csv
import os
import hashlib


def get_sha1_hash(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()


def evaluate_dictionary_attack_hibp_by_iteration():
    hibp_file = "pwnedpasswords.txt"

    print("⏳ HIBP 해시 데이터셋 장전 중...")
    hibp_set = set()
    try:
        with open(hibp_file, 'r', encoding='utf-8') as f:
            for line in f:
                hash_val = line.strip().split(':')[0]
                hibp_set.add(hash_val)
        print(f"✅ 총 {len(hibp_set):,}개 해시 장전 완료.\n")
    except FileNotFoundError:
        print(f"❌ '{hibp_file}' 파일이 없습니다.")
        return

    target_files = [
        "BaseLine/baseline_condition_passwords.csv",
        "Condition/Claude/claude_condition_fixed_passwords.csv",
        "Condition/Gemini/gemini_condition_fixed_passwords.csv",
        "Condition/GPT/gpt_condition_fixed_passwords.csv"
    ]

    print("🛡️ [HIBP 데이터셋 기반 회차별 사전 대입 공격 검사 결과]")
    print("=" * 70)

    for file_path in target_files:
        if not os.path.exists(file_path):
            continue

        # 데이터를 [회차][길이] 별로 담을 수 있는 2중 딕셔너리
        stats = {}

        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 앞선 코드에서 추가한 Iteration 컬럼을 읽어옵니다. (BaseLine 등 없는 경우 1회차로 간주)
                iteration = int(row.get('Iteration', 1))
                length = int(row['Length'])
                pwd = row['Password']

                if iteration not in stats:
                    stats[iteration] = {}
                if length not in stats[iteration]:
                    stats[iteration][length] = {'total': 0, 'leaked': 0, 'examples': []}

                stats[iteration][length]['total'] += 1

                pwd_hash = get_sha1_hash(pwd)
                if pwd_hash in hibp_set:
                    stats[iteration][length]['leaked'] += 1
                    if len(stats[iteration][length]['examples']) < 3:
                        stats[iteration][length]['examples'].append(pwd)

        print(f"📁 {file_path.split('/')[-1]}")

        # 1회차, 2회차, 3회차 순으로 출력
        for iteration in sorted(stats.keys()):
            print(f" 📌 [{iteration}회차 결과]")

            # 각 회차 안에서 8자, 12자, 16자 순으로 출력
            for length in sorted(stats[iteration].keys()):
                s = stats[iteration][length]
                total = s['total']
                leaked = s['leaked']

                if total > 0:
                    leak_rate = (leaked / total) * 100
                    safe_rate = 100 - leak_rate

                    print(f"   [길이: {length}자]")
                    print(f"     - 총 검사 개수: {total}개")
                    print(f"     - 유출 발견: {leaked}개 (취약도: {leak_rate:.2f}%)")
                    print(f"     - 🛡️ 방어율: {safe_rate:.2f}%")
                    if s['examples']:
                        print(f"     - 유출 예시: {', '.join(s['examples'])} ...")
            print("   " + "-" * 50)
        print("=" * 70)


if __name__ == "__main__":
    evaluate_dictionary_attack_hibp_by_iteration()