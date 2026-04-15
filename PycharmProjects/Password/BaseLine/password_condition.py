import secrets
import string
import csv


def generate_secure_password(length):
    """
    지정된 길이의 암호학적 난수 기반 비밀번호를 생성합니다.
    조건: 대문자, 소문자, 숫자, 특수문자 최소 1개 이상 포함
    """
    if length < 4:
        raise ValueError("비밀번호 길이는 최소 4 이상이어야 합니다.")

    # 사용할 문자열 집합 정의
    alphabet = string.ascii_letters + string.digits + string.punctuation

    while True:
        # secrets.choice를 사용하여 암호학적으로 안전한 난수 선택
        password = ''.join(secrets.choice(alphabet) for _ in range(length))

        # 조건 검사: 대문자, 소문자, 숫자, 특수문자가 모두 1개 이상 포함되었는지 확인
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in string.punctuation for c in password)):
            return password


def create_baseline_dataset(filename="baseline_condition_passwords.csv", count_per_length=300):
    """
    8자, 12자, 16자 길이에 대해 각각 지정된 개수만큼 비밀번호를 생성하고 CSV로 저장합니다.
    """
    lengths = [8, 12, 16]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # CSV 헤더 작성
        writer.writerow(["Length", "Password", "Type"])

        for length in lengths:
            for _ in range(count_per_length):
                pwd = generate_secure_password(length)
                writer.writerow([length, pwd, "Random_Baseline"])

    print(f"✅ {filename} 파일에 총 {len(lengths) * count_per_length}개의 베이스라인 비밀번호 저장이 완료되었습니다.")


# 코드 실행
if __name__ == "__main__":
    create_baseline_dataset(count_per_length=300)