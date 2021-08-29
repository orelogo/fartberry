#!/usr/bin/env python3
from typing import NamedTuple

import bme680

# Temperature in degree celsius
TEMPERATURE = 'temperature'
# Humidity in % relative humidity
HUMIDITY = 'humidity'
# Pressure in pascal
PRESSURE = 'pressure'

GasProperties = NamedTuple('GasProperties', [
    (TEMPERATURE, float),
    (HUMIDITY, float),
    (PRESSURE, float),
])


class _BME680Sensor():
    def __init__(self) -> None:

        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except RuntimeError:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        # These oversampling settings can be tweaked to
        # change the balance between accuracy and noise in
        # the data.

        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        self.sensor.set_gas_status(bme680.DISABLE_GAS_MEAS)
        # self.sensor.set_gas_heater_temperature(320)
        # self.sensor.set_gas_heater_duration(150)
        # self.sensor.select_gas_heater_profile(0)

    def get_gas_properties(self) -> GasProperties:
        self.sensor.get_sensor_data()

        gas_properties = GasProperties(
            **{
                TEMPERATURE: self.sensor.data.temperature,
                HUMIDITY: self.sensor.data.humidity,
                PRESSURE: self.sensor.data.pressure,
            })

        return gas_properties


bme_680_sensor = _BME680Sensor()
