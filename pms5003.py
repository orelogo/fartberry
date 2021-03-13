import serial
import datetime
from collections import namedtuple
from os import path

AirQuality = namedtuple('AirQuality', [
    'pm1_standard',   # PM 1.0 concentration in μg/m^3, corrected to standard atmophere conditions
    'pm25_standard',  # PM 2.5 concentration in μg/m^3, corrected to standard atmophere conditions
    'pm10_standard',  # PM 10 concentration in μg/m^3, corrected to standard atmophere conditions
    'pm1_ambient',    # PM 10 concentration in μg/m^3, in the current ambient conditions
    'pm25_ambient',   # PM 10 concentration in μg/m^3, in the current ambient conditions
    'pm10_ambient',   # PM 10 concentration in μg/m^3, in the current ambient conditions
    # number of particles with diameter >0.3 μm in 0.1 L (0.0001 m^3) of air
    'particles_03',
    # number of particles with diameter >0.5 μm in 0.1 L (0.0001 m^3) of air
    'particles_05',
    # number of particles with diameter >1.0 μm in 0.1 L (0.0001 m^3) of air
    'particles_1',
    # number of particles with diameter >2.5 μm in 0.1 L (0.0001 m^3) of air
    'particles_25',
    # number of particles with diameter >5.0 μm in 0.1 L (0.0001 m^3) of air
    'particles_5',
    # number of particles with diameter >10.0 μm in 0.1 L (0.0001 m^3) of air
    'particles_10',
])

BYTE_COUNT: int = 32
FIRST_BYTE: int = 0x42
SECOND_BYTE: int = 0x4d

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)


abs_log_path = path.join(path.dirname(__file__), "pms5003_log.txt")
log = open(abs_log_path, "a+")

try:
    while True:
        data: bytes = port.read(BYTE_COUNT)

        assert data[0] == FIRST_BYTE and data[1] == SECOND_BYTE, "Unexpected data received from sensor"

        air_quality = AirQuality(
            pm1_standard=int.from_bytes(data[4:6], byteorder='big'),
            pm25_standard=int.from_bytes(data[6:8], byteorder='big'),
            pm10_standard=int.from_bytes(data[8:10], byteorder='big'),
            pm1_ambient=int.from_bytes(data[10:12], byteorder='big'),
            pm25_ambient=int.from_bytes(data[12:14], byteorder='big'),
            pm10_ambient=int.from_bytes(data[14:16], byteorder='big'),
            particles_03=int.from_bytes(data[16:18], byteorder='big'),
            particles_05=int.from_bytes(data[18:20], byteorder='big'),
            particles_1=int.from_bytes(data[20:22], byteorder='big'),
            particles_25=int.from_bytes(data[22:24], byteorder='big'),
            particles_5=int.from_bytes(data[24:26], byteorder='big'),
            particles_10=int.from_bytes(data[26:28], byteorder='big'),
        )

        log.write(f"{str(datetime.datetime.now())} - {air_quality} \n") 
        log.flush()
        print(f"{str(datetime.datetime.now())} - {air_quality}")

except KeyboardInterrupt:
    print("Closing")
    log.close()