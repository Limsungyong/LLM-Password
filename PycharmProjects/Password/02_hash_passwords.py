import csv
import hashlib
from pathlib import Path

# =========================================================
# 프로젝트 외부 데이터 경로 설정
#
# 예시:
# D:\PasswordData\hashed
#
# 원본 txt는 프로젝트 내부 사용 가능
# =========================================================

# 비밀번호 txt 폴더들
INPUT_DIRS = [
    Path(r"YOUR_CONDITION_FOLDER"),
    Path(r"YOUR_SIMPLE_FOLDER")
]

# hashed csv 저장 폴더
OUTPUT_BASE = Path(r"YOUR_HASHED_OUTPUT_FOLDER")

OUTPUT_BASE.mkdir(parents=True, exist_ok=True)


def sha1_hash(password: str) -> str:
    return hashlib.sha1(
        password.encode("utf-8")
    ).hexdigest().upper()


def process_txt_file(txt_file: Path, relative_path: Path):

    output_dir = OUTPUT_BASE / relative_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    output_csv = output_dir / f"{txt_file.stem}.csv"

    print(f"처리 중: {txt_file}")

    count = 0

    with open(txt_file, "r", encoding="utf-8", errors="ignore") as infile, \
         open(output_csv, "w", newline="", encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "password",
            "length",
            "sha1",
            "prefix",
            "suffix"
        ])

        for line in infile:

            password = line.strip()

            if not password:
                continue

            sha1 = sha1_hash(password)

            writer.writerow([
                password,
                len(password),
                sha1,
                sha1[:5],
                sha1[5:]
            ])

            count += 1

            if count % 100_000 == 0:
                print(f"{count:,}개 처리 완료")

    print(f"완료: {output_csv}")
    print(f"총 {count:,}개\n")


def main():

    for input_dir in INPUT_DIRS:

        txt_files = list(input_dir.rglob("*.txt"))

        for txt_file in txt_files:

            relative_path = txt_file.relative_to(input_dir)

            process_txt_file(
                txt_file,
                Path(input_dir.name) / relative_path
            )

    print("전체 변환 완료")


if __name__ == "__main__":
    main()