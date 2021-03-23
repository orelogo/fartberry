#!/usr/bin/env python3
from collections import namedtuple

# PM 1.0 concentration in μg/m^3, corrected to standard atmophere conditions
PM1_STANDARD = 'pm1_standard'
# PM 2.5 concentration in μg/m^3, corrected to standard atmophere conditions
PM25_STANDARD = 'pm25_standard'
# PM 10 concentration in μg/m^3, corrected to standard atmophere conditions
PM10_STANDARD = 'pm10_standard'
# PM 10 concentration in μg/m^3, in the current ambient conditions
PM1_AMBIENT = 'pm1_ambient'
# PM 10 concentration in μg/m^3, in the current ambient conditions
PM25_AMBIENT = 'pm25_ambient'
# PM 10 concentration in μg/m^3, in the current ambient conditions
PM10_AMBIENT = 'pm10_ambient'
# number of particles with diameter >0.3 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_03 = 'particles_03'
# number of particles with diameter >0.5 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_05 = 'particles_05'
# number of particles with diameter >1.0 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_1 = 'particles_1'
# number of particles with diameter >2.5 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_25 = 'particles_25'
# number of particles with diameter >5.0 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_5 = 'particles_5'
# number of particles with diameter >10.0 μm in 0.1 L (0.0001 m^3) of air
PARTICLES_10 = 'particles_10'

ParticulateMatter = namedtuple('ParticulateMatter', [
    PM1_STANDARD,
    PM25_STANDARD,
    PM10_STANDARD,
    PM1_AMBIENT,
    PM25_AMBIENT,
    PM10_AMBIENT,
    PARTICLES_03,
    PARTICLES_05,
    PARTICLES_1,
    PARTICLES_25,
    PARTICLES_5,
    PARTICLES_10,
])
