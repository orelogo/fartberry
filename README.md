# Fartberry
Raspberry pi air quality monitor. Measures particulate matter in the air and stores values in Postgres SQL database along with geolocation data.

## Instructions
1. Install postgres database on raspberry pi and create a database for this project
2. Edit the config.json file with database details and preferences
3. Connect raspberry pi and PMS 5003 sensor correctly
4. `python3 fartberry.py`
