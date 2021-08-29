# Fartberry
Raspberry pi air quality monitor. Measures air temperature, humidity, pressure, and particulate matter in the air and stores values in Postgres SQL database along with geolocation data (optional). Used with the BME 680 sensor for air temperature, humidity and pressure, and the PMS 5003 sensor for particulate matter.

## Instructions
1. Install postgres database on raspberry pi and create a database for this project
2. Edit the `config.json` file with database details and preferences
3. Connect raspberry pi with the BME 680 and PMS 5003 sensor correctly
4. `pipenv run python3 -m fartberry`
