import csv
from pathlib import Path
from collections import defaultdict

# =========================================================
# 프로젝트 외부 데이터 경로 설정
#
# 예시:
# D:\PasswordData\pwned_checked
# D:\PasswordData\analysis
# =========================================================

# 03_lookup_with_sqlite.py 결과 폴더
CHECKED_DIR = Path(r"YOUR_PWNED_CHECKED_FOLDER")

# 분석 결과 저장 폴더
OUTPUT_DIR = Path(r"YOUR_ANALYSIS_OUTPUT_FOLDER")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 최종 요약 CSV
SUMMARY_CSV = OUTPUT_DIR / "summary_analysis.csv"


def analyze_file(csv_file: Path):

    total = 0
    pwned = 0
    total_pwned_count = 0

    length_stats = defaultdict(lambda: {
        "total": 0,
        "pwned": 0
    })

    with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:

        reader = csv.DictReader(f)

        for row in reader:

            total += 1

            length = int(row["length"])

            is_pwned = int(row["is_pwned"])

            pwned_count = int(row["pwned_count"])

            length_stats[length]["total"] += 1

            if is_pwned:

                pwned += 1
                total_pwned_count += pwned_count

                length_stats[length]["pwned"] += 1

    pwned_ratio = (
        pwned / total * 100
    ) if total else 0

    average_pwned_count = (
        total_pwned_count / pwned
    ) if pwned else 0

    return {
        "file_name": csv_file.name,
        "total_passwords": total,
        "pwned_passwords": pwned,
        "pwned_ratio_percent": round(pwned_ratio, 4),
        "average_pwned_count": round(average_pwned_count, 2),
        "length_stats": length_stats
    }


def main():

    checked_files = sorted(
        CHECKED_DIR.rglob("*_checked.csv")
    )

    if not checked_files:
        print("checked csv 파일이 없습니다.")
        return

    with open(
        SUMMARY_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as summary_file:

        writer = csv.writer(summary_file)

        writer.writerow([
            "file_name",
            "total_passwords",
            "pwned_passwords",
            "pwned_ratio_percent",
            "average_pwned_count"
        ])

        for checked_file in checked_files:

            result = analyze_file(checked_file)

            writer.writerow([
                result["file_name"],
                result["total_passwords"],
                result["pwned_passwords"],
                result["pwned_ratio_percent"],
                result["average_pwned_count"]
            ])

            print("=" * 60)
            print(f"파일: {result['file_name']}")
            print(f"전체 비밀번호 수: {result['total_passwords']:,}")
            print(f"유출 비밀번호 수: {result['pwned_passwords']:,}")
            print(
                f"유출 비율: "
                f"{result['pwned_ratio_percent']}%"
            )
            print(
                f"평균 유출 횟수: "
                f"{result['average_pwned_count']:,}"
            )

            print("\n[길이별 통계]")

            for length, stats in sorted(
                result["length_stats"].items()
            ):

                ratio = (
                    stats["pwned"] /
                    stats["total"] * 100
                ) if stats["total"] else 0

                print(
                    f"{length}자리 | "
                    f"전체 {stats['total']:,}개 | "
                    f"유출 {stats['pwned']:,}개 | "
                    f"{ratio:.4f}%"
                )

            print()

    print("=" * 60)
    print("전체 분석 완료")
    print(f"요약 CSV 위치:")
    print(SUMMARY_CSV)


if __name__ == "__main__":
    main()