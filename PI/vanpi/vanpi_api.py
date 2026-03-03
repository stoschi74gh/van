from fastapi import FastAPI
import sqlite3
from config import DB_PATH

app = FastAPI()

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 1. THE DASHBOARD ENDPOINT (Latest for every sensor)
@app.get("/latest")
def get_latest():
    conn = get_connection()
    # This query finds the single most recent reading for EVERY sensor in your DB
    query = """
        SELECT 
            s.name AS sensor_name, 
            s.model AS sensor_model,
            r.value1, r.value2, r.value3, r.timestamp
        FROM sensors s
        JOIN readings r ON r.id = (
            SELECT id FROM readings 
            WHERE sensor_id = s.id 
            ORDER BY timestamp DESC LIMIT 1
        )
        WHERE s.active = 1
    """
    rows = conn.execute(query).fetchall()
    conn.close()

    result = {}
    for row in rows:
        result[row["sensor_name"]] = {
            "model": row["sensor_model"],
            "timestamp": row["timestamp"],
            "values": {
                "v1": row["value1"],
                "v2": row["value2"],
                "v3": row["value3"]
            }
        }
    return result if result else {"error": "No data"}

# 2. THE GRAPH ENDPOINT (7-day history for a specific sensor)
@app.get("/history/{sensor_name}")
def get_history(sensor_name: str):
    try:
        conn = get_connection()
        # Explicitly naming columns in the second SELECT to match the first
        query = """
SELECT 
    h.avg_value1 as v1, 
    h.avg_value2 as v2, 
    h.avg_value3 as v3, 
    h.hour as timestamp
FROM hourly_readings h
JOIN sensors s ON h.sensor_id = s.id
WHERE s.name = ?
  AND h.hour >= datetime('now', '-7 days')
ORDER BY h.hour ASC
       """
        rows = conn.execute(query, (sensor_name,)).fetchall()
        conn.close()
        
        # Convert to list of dicts
        return [dict(row) for row in rows]
    except Exception as e:
        # This print will show up in your Raspberry Pi terminal!
        print(f"CRITICAL API ERROR: {e}")
        return {"error": str(e)}
