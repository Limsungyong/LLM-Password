import sqlite3
from pathlib import Path

# =========================================================
# 프로젝트 외부 데이터 경로 설정
#
# 예시:
# D:\PasswordData\split
# D:\PasswordData\pwned_passwords.sqlite
# =========================================================

# HIBP split txt 폴더 경로
SPLIT_DIR = Path(r"YOUR_SPLIT_FOLDER")

# 생성될 SQLite DB 파일 경로
DB_PATH = Path(r"YOUR_DB_FILE.sqlite")

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

BATCH_SIZE = 100_000


def create_database(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pwned_passwords (
            sha1 TEXT PRIMARY KEY,
            count INTEGER
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sha1
        ON pwned_passwords(sha1)
    """)


def insert_batch(cursor, conn, batch):
    cursor.executemany("""
        INSERT OR REPLACE INTO pwned_passwords
        (sha1, count)
        VALUES (?, ?)
    """, batch)

    conn.commit()


def main():

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # SQLite 성능 최적화
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA temp_store=MEMORY")
    cursor.execute("PRAGMA cache_size=-200000")

    create_database(cursor)

    txt_files = sorted(SPLIT_DIR.glob("*.txt"))

    if not txt_files:
        print("split txt 파일이 없습니다.")
        return

    total_count = 0
    batch = []

    for txt_file in txt_files:

        prefix = txt_file.stem.upper()

        print(f"처리 중: {txt_file.name}")

        with open(txt_file, "r", encoding="utf-8", errors="ignore") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                try:
                    suffix, count = line.split(":")
                except ValueError:
                    continue

                sha1 = prefix + suffix

                batch.append((
                    sha1,
                    int(count)
                ))

                total_count += 1

                if len(batch) >= BATCH_SIZE:

                    insert_batch(
                        cursor,
                        conn,
                        batch
                    )

                    print(
                        f"{total_count:,}개 저장 완료"
                    )

                    batch.clear()

    if batch:

        insert_batch(
            cursor,
            conn,
            batch
        )

    conn.close()

    print("=" * 60)
    print("SQLite DB 생성 완료")
    print(f"총 저장 수: {total_count:,}")
    print(f"DB 위치:")
    print(DB_PATH)


if __name__ == "__main__":
    main()