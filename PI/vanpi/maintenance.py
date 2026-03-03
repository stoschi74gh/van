import sys
import sqlite3
import shutil
import os
from datetime import datetime

DB_PATH = "/home/stefpi/vanpi/vanpi.db"
BACKUP_DIR = "/home/stefpi/vanpi/backups"
RETENTION_DAYS = 30
MAX_BACKUPS = 7

os.makedirs(BACKUP_DIR, exist_ok=True)

def rotate_backups():
    backups = sorted(
        [f for f in os.listdir(BACKUP_DIR) if f.startswith("vanpi_backup_")],
        reverse=True
    )
    for old_backup in backups[MAX_BACKUPS:]:
        os.remove(os.path.join(BACKUP_DIR, old_backup))
        print(f"Deleted old backup: {old_backup}")

def backup_db():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"vanpi_backup_{timestamp}.db")
    shutil.copy2(DB_PATH, backup_file)
    print(f"Database backed up to {backup_file}")
    rotate_backups()
    return backup_file

def aggregate_hourly(conn):
    print(f"[{datetime.now()}] Updating hourly averages...")
    c = conn.cursor()
    conn.execute("""
	CREATE TABLE IF NOT EXISTS hourly_readings (
    	    id INTEGER PRIMARY KEY,
    	    sensor_id INTEGER,
    	    hour DATETIME,
    	    avg_value1 REAL,
    	    avg_value2 REAL,
    	    avg_value3 REAL,
	    UNIQUE(sensor_id, hour),
	    FOREIGN KEY(sensor_id) REFERENCES sensors(id)
        )
    """ )
    
    conn.execute("""
        INSERT OR IGNORE INTO hourly_readings (sensor_id, hour, avg_value1, avg_value2, avg_value3)
        SELECT
            sensor_id,
            strftime('%Y-%m-%d %H:00:00', timestamp) as hour,
            AVG(value1),
            AVG(value2),
            AVG(value3)
        FROM readings
        GROUP BY sensor_id, hour
    """)
    conn.commit()
    print("Hourly aggregation updated.")

def delete_old_raw(conn):
    c = conn.cursor()
    c.execute(f"""
    DELETE FROM readings
    WHERE timestamp < datetime('now', '-{RETENTION_DAYS} days')
    """)
    conn.commit()
    print("Old raw readings deleted.")

def main():
    print("Starting maintenance...")
    backup_file = backup_db()

    conn = sqlite3.connect(DB_PATH)
    try:
        aggregate_hourly(conn)
        delete_old_raw(conn)
    except Exception as e:
        print(f"Error during maintenance: {e}")
        print("Restoring from backup...")
        shutil.copy2(backup_file, DB_PATH)
    finally:
        conn.close()
    print("Maintenance complete.")

def ensure_metadata_table(conn):
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS system_metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()

def get_last_maintenance_date(conn):
    c = conn.cursor()
    c.execute("SELECT value FROM system_metadata WHERE key = 'last_maintenance'")
    row = c.fetchone()
    return row[0] if row else None


def set_last_maintenance_date(conn, date_str):
    c = conn.cursor()
    c.execute("""
        INSERT INTO system_metadata (key, value)
        VALUES ('last_maintenance', ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """, (date_str,))
    conn.commit()

def vacuum_database(conn):
    print("Running VACUUM...")
    conn.execute("VACUUM")
    print("VACUUM complete.")

def ensure_indexes(conn):
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_readings_timestamp
        ON readings(timestamp)
    """)
    conn.commit()

def run_maintenance():
    conn = sqlite3.connect(DB_PATH)
    ensure_metadata_table(conn)
    ensure_indexes(conn)
    today = datetime.now().date().isoformat()
    now = datetime.now()
    current_hour = now.hour
    last_run = get_last_maintenance_date(conn)

    print("Starting maintenance...")

    try:
        aggregate_hourly(conn)
        if current_hour == 3:
            backup_file = backup_db()
            delete_old_raw(conn)
            vacuum_database(conn)
            set_last_maintenance_date(conn, today)

    except Exception as e:
        print(f"Error during maintenance: {e}")
        print("Restoring from backup...")
        conn.close()
        shutil.copy2(backup_file, DB_PATH)
        return

    conn.close()
    print("Maintenance complete.")


if __name__ == "__main__":
    run_maintenance()

