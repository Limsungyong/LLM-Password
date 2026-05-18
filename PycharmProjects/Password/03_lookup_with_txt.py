import csv
from pathlib import Path
from collections import defaultdict

# =========================================================
# 프로젝트 외부 데이터 경로 설정
#
# 예시:
# D:\PasswordData\hashed
# D:\PasswordData\split
# D:\PasswordData\pwned_checked
# =========================================================

# 02_hash_passwords.py 결과 CSV 폴더
HASHED_DIR = Path(r"")

# HIBP 공식 split txt 폴더
PWNED_SPLIT_DIR = Path(r"")

# 검사 결과 저장 폴더
OUTPUT_BASE = Path(r"")

OUTPUT_BASE.mkdir(parents=True, exist_ok=True)


def load_pwned_prefix(prefix: str):
    """
    해당 prefix txt 파일을 한 번만 읽어서
    suffix -> count 딕셔너리로 변환
    """
    target_file = PWNED_SPLIT_DIR / f"{prefix}.txt"

    suffix_map = {}

    if not target_file.exists():
        return suffix_map

    with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                suffix, count = line.split(":")
                suffix_map[suffix] = int(count)
            except ValueError:
                continue

    return suffix_map


def process_csv(csv_file: Path):
    relative_path = csv_file.relative_to(HASHED_DIR)

    output_dir = OUTPUT_BASE / relative_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    output_csv = output_dir / f"{csv_file.stem}_checked.csv"

    if output_csv.exists():
        print(f"이미 존재함 - 건너뜀: {output_csv.name}")
        return

    print(f"검사 시작: {csv_file.name}")

    # 1단계: hashed CSV를 prefix별로 묶기
    prefix_groups = defaultdict(list)

    with open(csv_file, "r", encoding="utf-8", errors="ignore") as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            prefix_groups[row["prefix"]].append(row)

    checked = 0
    pwned = 0

    # 2단계: prefix 파일 하나씩만 열어서 비교
    with open(output_csv, "w", newline="", encoding="utf-8") as outfile:
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

        for prefix, rows in prefix_groups.items():
            suffix_map = load_pwned_prefix(prefix)

            for row in rows:
                suffix = row["suffix"]

                count = suffix_map.get(suffix, 0)
                is_pwned = 1 if count > 0 else 0

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

                if is_pwned:
                    pwned += 1

                # 진행률 출력
                if checked % 100_000 == 0:
                    print(
                        f"{csv_file.name} | "
                        f"{checked:,}개 검사 완료 | "
                        f"유출 {pwned:,}개"
                    )

    print(
        f"완료: {output_csv.name} | "
        f"검사 {checked:,}개 | "
        f"유출 {pwned:,}개\n"
    )


def main():
    csv_files = sorted(HASHED_DIR.rglob("*.csv"))

    if not csv_files:
        print("hashed csv 파일이 없습니다.")
        return

    for csv_file in csv_files:
        process_csv(csv_file)

    print("=" * 60)
    print("전체 txt 기반 조회 완료")


if __name__ == "__main__":
    main()