import sqlite3
from config import DB_PATH
from datetime import datetime, timedelta, timezone

STALE_MINUTES = 2

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name, last_seen FROM devices")
rows = cursor.fetchall()


now = datetime.now(timezone.utc)

for name, last_seen in rows:
	if not last_seen:
		print(f"{name}: NEVER SEEN")
		continue

	last_seen_dt = datetime.fromisoformat(last_seen).replace(tzinfo=timezone.utc)
	if now - last_seen_dt > timedelta(minutes=STALEMINUTES):
		print(f"{name}: STALE")
	else:
		print(f"{name}: OK")
