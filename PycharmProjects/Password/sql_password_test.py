import sqlite3
from pathlib import Path

DB_PATH = Path(r"D:\Code\심화과정\논문\data\splitDB\pwned_passwords.sqlite")

test_hashes = {
    "password": "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8",
    "123456": "7C4A8D09CA3762AF61E59520943DC26494F8941B",
    "password123": "CBFDAC6008F9CAB4083784CBD1874F76618D2A97",
}

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

for pw, sha1 in test_hashes.items():
    cur.execute(
        "SELECT count FROM pwned_passwords WHERE sha1 = ?",
        (sha1,)
    )
    result = cur.fetchone()
    print(pw, result)

conn.close()