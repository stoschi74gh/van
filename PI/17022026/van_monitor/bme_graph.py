#!/usr/bin/env python3

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- calculate the altitude from pressure ---
def pressure_to_altitude(pressure_hpa, sea_level_pressure=1013.25):
	"""
	Calculate altitude in meters from pressure in hPa.
	"""
	return 44330.0 * (1.0 - (pressure_hpa / sea_level_pressure) **(1/5.255))



# --- input from user ---

while True:
	time_range_type = input("Choose the time range type (H=Hours, D=Days, M=Months: ").upper()
	if time_range_type not in ["H", "D", "M"]:
		print("Invalid option. Please enter H, D or M only.")
		continue

	time_range_qty = input("How many? ").strip()
	if not time_range_qty.isdigit():
		print("Please enter a valid positive number.")
		continue

	time_range_qty = int(time_range_qty)
	if time_range_qty <= 0:
		print("umber must be greater than zero")
		continue
	break

# --- build interval ---
if time_range_type == "H":
	interval = f"-{time_range_qty} hours"
elif time_range_type == "D":
        interval = f"-{time_range_qty} days" 
elif time_range_type == "M":
        interval = f"-{time_range_qty} months" 

# --- config ---
DB_FILE = '/home/stefpi/van_monitor/bme_database.db'
GRAPH_FILE = '/home/stefpi/van_monitor/bme_graph.png'

# --- read data ---
conn = sqlite3.connect(DB_FILE)
query = f"""
SELECT timestamp, temperature, humidity, pressure
FROM bme_log
WHERE timestamp >= datetime('now', '{interval}')
ORDER BY timestamp ASC
"""

df = pd.read_sql_query(query, conn)
conn.close()

#stop if no data
if df.empty:
	print("No data found for the selected range.")
	exit()

# --- convert timestamp ---
df['timestamp'] = pd.to_datetime(df['timestamp'])

# --- plot ---
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['temperature'], label = 'Temperature (C)', color='red')
plt.plot(df['timestamp'], df['humidity'], label = 'Humidity (%)', color='blue')
plt.plot(df['timestamp'], df['pressure']*0.000987*10, label = 'Pressure (atm*10)', color='green')
altitude = pressure_to_altitude(df['pressure'])
plt.plot(df['timestamp'], altitude/10, label = 'Altitude (m/10)', color='orange')


plt.xlabel('Time')
plt.ylabel('Sensor values')
plt.title(f'BME280 Sensor Data - Last {interval}')
plt.legend()
plt.grid(True)
plt.tight_layout()

# --- show & save ---
plt.savefig(GRAPH_FILE)
plt.show()
print(f"Graph saved to {GRAPH_FILE}")
