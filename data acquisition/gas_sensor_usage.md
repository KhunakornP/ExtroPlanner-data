# How to use the MQ-9 Gas sensor

First off, to whomever finds this document. If you are trying to use this sensor to detect
co for health purposes you are using the wrong sensor.<br>

The MQ-9 sensor has a sensitivity range of 10-10000 ppm as per the specifications I could find.
The range of 10-10000 ppm is not guaranteed as each different manufacturer has different specifications.<br>

If you are looking to measure co in the ranges of 0-1000 I recommend these sensors.
- [The MICS-5524 sensor](https://www.arduitronics.com/product/4234/mics-5524-air-quality-gas-sensor-module-mics5524-co-alcohol-and-voc-gas-sensor-module)
- [The ZE07 sensor](https://www.arduitronics.com/product/4334/ze07-co-electrochemical-carbon-monoxide-co-sensor-module-โมดูลตรวจจับคาร์บอนมอนอกไซด์-โดยใช้-electro)

These sensors have a precision of .0 and are more suitable for early warning and for measuring Outdoor CO levels.
The MQ-9 sensor is extremely insensitive and is more suited for a Fire detection system.<br>

With that note out of the way.

# How to calibrate the MQ-9 Gas sensor

You will need to preheat the sensor for 1-2 days per the specification but a 6-hour warmup is sufficient for calibration purposes.<br>

The `sensor_calibration.py` file checks the reading of the sensor. Run the script until the adc measurement is steady.

If you wish to derive your own formula, https://web.archive.org/web/20220820214914/https://programozdazotthonod.hu/2020/05/03/a-proper-guide-to-the-mq9-sensor/ has a good tutorial on it.

# How the MQ-9 Gas sensor functions

It is a MOS (metal oxide semiconductor) sensor, which uses a Burn-off method to read the values.
You will need to supply the sensor with 5v of power and periodically change the voltage to 1.4v.
This can be done by changing the supplied voltage, but you will need to take into account the change in voltage for calculations.
Alternatively, a voltage control circuit which changes the heater's voltage would be better.
You read the values during the low 1.4v periods (60 s) and burn off the sensor to reset the sensor's value at 5v (90 s)
