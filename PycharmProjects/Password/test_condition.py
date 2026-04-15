import csv
import math
from collections import Counter
from itertools import combinations


def calculate_shannon_entropy(password):
    """문자열의 섀넌 엔트로피를 계산합니다. (무작위성 지표)"""
    if not password:
        return 0
    entropy = 0
    length = len(password)
    # 문자의 등장 빈도를 계산
    frequencies = Counter(password)

    for count in frequencies.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    return entropy


def calculate_jaccard_similarity(str1, str2):
    """두 문자열 간의 자카드 유사도를 계산합니다. (문자 집합의 유사성)"""
    set1, set2 = set(str1), set(str2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0


def calculate_levenshtein_distance(s1, s2):
    """두 문자열 간의 레벤슈타인 거리를 계산합니다. (몇 글자를 고쳐야 같아지는지 측정)"""
    if len(s1) < len(s2):
        return calculate_levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def evaluate_dataset(filename="baseline_passwords.csv"):
    """CSV 파일을 읽어 각 길이별로 평가 지표와 실제 중복된 비밀번호를 분석합니다."""
    passwords_by_length = {8: [], 12: [], 16: []}

    try:
        with open(filename, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                length = int(row['Length'])
                password = row['Password']
                if length in passwords_by_length:
                    passwords_by_length[length].append(password)
    except FileNotFoundError:
        print(f"❌ '{filename}' 파일을 찾을 수 없습니다.")
        return

    print(f"📊 '{filename}' 평가 결과 요약")
    print("=" * 70)
    print(f"{'Length':<8} | {'Avg Entropy':<12} | {'Duplication (%)':<16} | {'Avg Levenshtein':<15}")
    print("-" * 70)

    for length, passwords in passwords_by_length.items():
        total_count = len(passwords)
        if total_count == 0:
            continue

        entropies = [calculate_shannon_entropy(p) for p in passwords]
        avg_entropy = sum(entropies) / total_count

        unique_passwords = set(passwords)
        duplication_rate = ((total_count - len(unique_passwords)) / total_count) * 100

        sample_pairs = list(combinations(passwords[:50], 2))
        levenshtein_dists = [calculate_levenshtein_distance(p1, p2) for p1, p2 in sample_pairs]
        avg_levenshtein = sum(levenshtein_dists) / len(levenshtein_dists) if levenshtein_dists else 0

        # 1. 기본 수치 출력
        print(f"{length:<8} | {avg_entropy:<12.4f} | {duplication_rate:<16.2f} | {avg_levenshtein:<15.4f}")

        # ---------------------------------------------------------
        # 🌟 실제 중복된 비밀번호 찾기 및 출력
        # ---------------------------------------------------------
        password_counts = Counter(passwords)
        duplicates = {pwd: count for pwd, count in password_counts.items() if count > 1}

        if duplicates:
            sorted_dups = sorted(duplicates.items(), key=lambda x: x[1], reverse=True)
            print(f"  🚨 [중복 발생 알림] 가장 많이 중복된 Top 5 (길이 {length}):")
            for pwd, count in sorted_dups[:5]:
                print(f"      - '{pwd}' : {count}회 생성됨")
        else:
            print(f"  ✅ 중복된 비밀번호 없음 (Clean!)")
        print("-" * 70)
    print("💡 분석 가이드:")
    print(" - Avg Entropy (엔트로피): 문자열의 무작위성입니다. 값이 높을수록 예측하기 어렵습니다. 만점 : 8자(3.0점), 12자(3.5점), 16자(4.0점)")
    print(" - Duplication (중복률): 동일한 비밀번호가 생성된 비율입니다. (난수 기반은 0%가 정상)")
    print(" - Avg Levenshtein (레벤슈타인 거리): 비밀번호 간의 형태적 거리입니다. 높을수록 서로 다르게 생겼다는 뜻입니다.")


# ---------------------------------------------------------
# 실행 부분: 새 폴더 구조(Simple)에 맞게 경로 업데이트!
# ---------------------------------------------------------
if __name__ == "__main__":

    # 💡 포인트: BaseLine(정답지)도 같이 넣어서 AI 결과와 한눈에 비교할 수 있게 했습니다.
    target_files = [
        "BaseLine/baseline_condition_passwords.csv",  # 파이썬 조건형 난수
        "Condition/Claude/claude_condition_fixed_passwords.csv",  # Claude 결과
        "Condition/Gemini/gemini_condition_fixed_passwords.csv",  # Gemini 결과
        "Condition/GPT/gpt_condition_fixed_passwords.csv",  # GPT 결과
        "Condition/Perplexity/perplexity_condition_fixed_passwords.csv"  # Perplexity 결과
    ]

    for file in target_files:
        print(f"\n🚀 [{file}] 분석 시작...")
        evaluate_dataset(file)
        print("\n" + "=" * 80 + "\n")