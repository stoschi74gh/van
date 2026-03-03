import sqlite3
from config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_or_create_device(conn, device_name):
    cur = conn.cursor()
    cur.execute("SELECT id FROM devices WHERE name=?", (device_name,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute("INSERT INTO devices (name) VALUES (?)", (device_name,))
    conn.commit()
    return cur.lastrowid

def get_or_create_sensor(conn, device_id, sensor_name, model):
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM sensors WHERE device_id=? AND name=?",
        (device_id, sensor_name),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        "INSERT INTO sensors (device_id, name, model) VALUES (?, ?, ?)",
        (device_id, sensor_name, model),
    )
    conn.commit()
    return cur.lastrowid

def insert_reading(conn, sensor_id, values):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO readings (sensor_id, value1, value2, value3) VALUES (?, ?, ?, ?)",
        (
            sensor_id,
            values[0] if len(values) > 0 else None,
            values[1] if len(values) > 1 else None,
            values[2] if len(values) > 2 else None,
        ),
    )
    conn.commit()

def update_last_seen(conn, device_id, sensor_id):
	cursor = conn.cursor()
	cursor.execute(
		"UPDATE devices SET last_seen=CURRENT_TIMESTAMP WHERE id=?",
		(device_id),
	)

	cursor.execute(
		"UPDATE sensors SET last_seen=CURRENT_TIMESTAMP WHERE id=?",
		(sensor_id),
	)
	conn.commit()

