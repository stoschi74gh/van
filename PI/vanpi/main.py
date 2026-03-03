import time
import serial
import sys
import maintenance
from datetime import datetime
from config import SERIAL_PORT, BAUDRATE
from database import (
    get_connection,
    get_or_create_device,
    get_or_create_sensor,
    insert_reading,
)
from parser import parse_line

print("START OF THE PROGRAM")


last_maintenance_day = None


def connect_serial():
	while True:
		try:
			print("Connecting to serial:", SERIAL_PORT)
			ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
			ser.setDTR(False)
			time.sleep(2)
			ser.flushInput()
			ser.setDTR(True)
			time.sleep(0.5)
			print("Serial connected.")
			return ser

		except serial.SerialException as e:
			print("Serial connection failed:", e)
		time.sleep(5)


def run():
	conn = get_connection()
	ser = connect_serial()

	last_valid_read = time.time()
	STALE_TIMEOUT = 300 #seconds
	MAX_RECOVERY_ATTEMPTS = 3
	recovery_attempts = 0

#	while True:
#    		raw = ser.readline()
#    		print("RAW BYTES:", raw)
#    		time.sleep(1)


	while True:
		try:
			#print("INSIDE THE LOOP")
			raw_bytes = ser.readline()
			#print("RAW BYTES:", repr(raw_bytes))
			line = raw_bytes.decode("utf-8", errors="ignore").strip()
			#print("RAW:", repr(line))
			if not line:
				print("No line received from serial")
				time.sleep(5)
				continue

			
			parsed = parse_line(line)
			if not parsed:
				print("Invalid format")
				continue
			else:
				print("Valid: ", parsed)
				

			device_name, sensor_name, model, values = parsed
		
			device_id = get_or_create_device(conn, device_name)
			sensor_id = get_or_create_sensor(conn, device_id, sensor_name, model)
			insert_reading(conn, sensor_id, values)
			update_last_seen(conn, device_id, sensor_id)
			last_valid_read =time.time() #heartbeat
			recovery_attempts = 0

			print("Inserted:", device_name, sensor_name, values)

		except serial.SerialException as e:
			print("Serial error:", e)
			ser.close()
			time.sleep(2)
			ser = connect_serial()
		except Exception as e:
                        print("Unexpected error:", e)
                        time.sleep(2)

		# --- STALE CHECK ---
		if time.time() - last_valid_read > STALE_TIMEOUT:
			recovery_attempts += 1
			print(f"Stale detected. Attempt {recovery_attempts}.")

			if recovery_attempts <= MAX_RECOVERY_ATTEMPTS:
				print("Soft reconnecting serial...")
				ser.close()
				time.sleep(2)
				ser = connect_serial()
				last_valid_read = time.time()
			else:
				print("Max recovery attempts reached. Exiting for systemd restart.")
				sys.exit(1)

		#running maintenance (executes only one time per day, date saved into the db)
		maintenance.run_maintenance()



if __name__ == "__main__":
	try:
		run()
	except KeyboardInterrupt:
		print("Shutting down...")
		sys.exit(0)
