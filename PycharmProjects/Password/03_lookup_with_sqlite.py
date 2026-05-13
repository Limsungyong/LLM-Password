import csv
import sqlite3
from pathlib import Path

# =========================================================
# 프로젝트 외부 데이터 경로 설정
#
# 예시:
# D:\PasswordData\hashed
# D:\PasswordData\pwned_passwords.sqlite
# D:\PasswordData\pwned_checked
# =========================================================

# 02_hash_passwords.py 결과 CSV 폴더
HASHED_DIR = Path(r"YOUR_HASHED_FOLDER")

# 01_make_pwned_sqlite_from_split.py 에서 생성한 DB
DB_PATH = Path(r"YOUR_DB_FILE.sqlite")

# 검사 결과 저장 폴더
OUTPUT_BASE = Path(r"YOUR_PWNED_CHECKED_FOLDER")

OUTPUT_BASE.mkdir(parents=True, exist_ok=True)


def process_csv(csv_file: Path, cursor):

    relative_path = csv_file.relative_to(HASHED_DIR)

    output_dir = OUTPUT_BASE / relative_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    output_csv = output_dir / f"{csv_file.stem}_checked.csv"

    print(f"검사 시작: {csv_file.name}")

    checked = 0
    pwned = 0

    with open(csv_file, "r", encoding="utf-8", errors="ignore") as infile, \
         open(output_csv, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        writer.writerow([
            "password",
            "length",
            "sha1",
            "prefix",
            "suffix",
            "is_pwned",
            "pwned_count"
        ])

        for row in reader:

            sha1 = row["sha1"].upper()

            cursor.execute(
                """
                SELECT count
                FROM pwned_passwords
                WHERE sha1 = ?
                """,
                (sha1,)
            )

            result = cursor.fetchone()

            if result:
                is_pwned = 1
                count = result[0]
                pwned += 1
            else:
                is_pwned = 0
                count = 0

            writer.writerow([
                row["password"],
                row["length"],
                row["sha1"],
                row["prefix"],
                row["suffix"],
                is_pwned,
                count
            ])

            checked += 1

            if checked % 10_000 == 0:
                print(
                    f"{checked:,}개 검사 완료 "
                    f"/ 유출 {pwned:,}개"
                )

    print(
        f"완료: {output_csv.name} | "
        f"검사 {checked:,}개 | "
        f"유출 {pwned:,}개\n"
    )


def main():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    csv_files = sorted(
        HASHED_DIR.rglob("*.csv")
    )

    if not csv_files:
        print("hashed csv 파일이 없습니다.")
        return

    for csv_file in csv_files:
        process_csv(csv_file, cursor)

    conn.close()

    print("=" * 60)
    print("전체 SQLite 조회 완료")


if __name__ == "__main__":
    main()