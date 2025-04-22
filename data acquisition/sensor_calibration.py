import machine
from machine import ADC, Pin
import time
import math

adc = ADC(Pin(32))


def read_mq9(adc):
    CO_gas = 0
    adc_val = 0
    time.sleep(90)
    for i in range(60):
        uv_value = adc.read_uv()
        adc_read = adc.read()
        voltage = uv_value/10**6
        CO_gas += 595 * pow(((5/voltage)-1)*(996/850),-2.24)
        adc_val += adc_read
        time.sleep(1)
    return CO_gas/60, adc_val/60 if adc_val > 0 else 0

try:
    while True:
        co_value, adc_avg = read_mq9(adc)
        print(f"adc_avg: {adc_avg}")
        print(f"co_read: {co_value} ")
        print("===============================")
        time.sleep(5)
except KeyboardInterrupt:
    print("Program stopped")