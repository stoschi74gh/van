The structure is working for /home/stefpi/vanpi, all files are stored in this folder
Any change to path, needs to be checked/updated in the code.

./services			contains the files to be copied to /etc/systemd/system and be ran as services

in ./services
vanpi_logger.services		triggers
vanpi-maintenance.timer		triggers vanpi-maintenance.services once/day at 3 am if pi is on. if not, as soon as it boots up	
vanpi-maintenance.service	triggers maintenance.py

in ./
config.py			configuration parameters (paths and settings)
database.py			the sqlite3 database keeping the history of the readings
health_check.py			heartbeat and checks
init.db				runs the first time, to generate the tables inside the db
main.py				entry point.
maintenance.py			creates a backup into ./backups, 
				cleans up old backups, 
				logs to db the average readings by hour for the readings older than one month, 
				to reduce the weight of the historical data
parser.py			parses the readings
run_logger.py			gets data from readings to the db
vanpi_api			serves data to be read by the app
