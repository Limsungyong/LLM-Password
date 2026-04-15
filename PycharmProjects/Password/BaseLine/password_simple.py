import secrets
import string
import csv


def generate_simple_password(length):
    """조건 없이 완전히 무작위로만 뽑는 단순형 난수 비밀번호"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # 조건 검사 없이 뽑힌 그대로 바로 반환!
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_simple_baseline(filename="baseline_simple_passwords.csv", count_per_length=500):
    lengths = [8,12,16]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Length", "Password", "Type"])
        for length in lengths:
            for _ in range(count_per_length):
                pwd = generate_simple_password(length)
                writer.writerow([length, pwd, "Random_Simple_Baseline"])
    print(f"{filename} 생성 완료!")

if __name__ == "__main__":
    create_simple_baseline()