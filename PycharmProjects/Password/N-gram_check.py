import csv
import os
from collections import Counter


def analyze_entropy_illusion_detailed():
    # 1. RockYou 데이터셋 로드 (기존 로직)
    rockyou_file = "rockyou.txt"
    print("⏳ RockYou 데이터셋 장전 중...")
    try:
        with open(rockyou_file, 'r', encoding='latin-1') as f:
            rockyou_set = set(line.strip() for line in f)
        print(f"✅ 총 {len(rockyou_set):,}개 장전 완료.\n")
    except FileNotFoundError:
        print(f"❌ '{rockyou_file}' 파일이 없습니다. 유출 검사는 제외하고 분석합니다.")
        rockyou_set = set()

    # 분석 대상 파일 리스트
    target_files = [
        "BaseLine/baseline_condition_passwords.csv",
        "Condition/Claude/claude_condition_fixed_passwords.csv",
        "Condition/Gemini/gemini_condition_fixed_passwords.csv",
        "Condition/GPT/gpt_condition_fixed_passwords.csv",
        "Simple/Claude/claude_simple_fixed_passwords.csv",
        "Simple/Gemini/gemini_simple_fixed_passwords.csv",
        "Simple/GPT/gpt_simple_fixed_passwords.csv",
    ]

    print("📊 [비밀번호 구조적 편향성 및 N-gram 분석 결과]")
    print("=" * 80)

    for file_path in target_files:
        if not os.path.exists(file_path):
            continue

        total_count = 0
        leaked_count = 0
        first_chars = []
        trigrams = []  # 3-gram 저장

        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                pwd = str(row['Password'])
                if not pwd: continue

                total_count += 1

                # 유출 검사
                if pwd in rockyou_set:
                    leaked_count += 1

                # ① 첫 글자 추출 (분포 분석용)
                first_chars.append(pwd[0])

                # ② 3-gram 추출 (연속 패턴 분석용)
                # 예: 'Pass123' -> 'Pas', 'ass', 'ss1', '123'
                for i in range(len(pwd) - 2):
                    trigrams.append(pwd[i:i + 3])

        if total_count > 0:
            # 첫 글자 분포 계산
            first_char_counts = Counter(first_chars)
            # 3-gram 상위 5개 계산
            top_trigrams = Counter(trigrams).most_common(5)

            # 첫 글자 유형(대문자/숫자/소문자) 비율 계산
            categories = {"Upper": 0, "Lower": 0, "Digit": 0, "Special": 0}
            for char in first_chars:
                if char.isupper():
                    categories["Upper"] += 1
                elif char.islower():
                    categories["Lower"] += 1
                elif char.isdigit():
                    categories["Digit"] += 1
                else:
                    categories["Special"] += 1

            print(f"📁 파일: {file_path.split('/')[-1]}")
            print(f"   - 총 검사: {total_count}개 | 유출: {leaked_count}개")

            print(f"   [A] 첫 글자 시작 유형 분포:")
            for cat, count in categories.items():
                percentage = (count / total_count) * 100
                print(f"       * {cat}: {percentage:.2f}% ({count}개)")

            print(f"   [B] 상위 5개 빈도 패턴 (3-gram):")
            for pattern, count in top_trigrams:
                p_rate = (count / len(trigrams)) * 100
                print(f"       * '{pattern}': {count}회 출현 ({p_rate:.3f}%)")

            print("-" * 80)


if __name__ == "__main__":
    analyze_entropy_illusion_detailed()