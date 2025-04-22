import time
import json
import network
import asyncio
import machine
from machine import Pin, I2C, ADC
from umqtt.robust import MQTTClient
from config import (
WIFI_SSID, WIFI_PASS,
MQTT_BROKER, MQTT_USER, MQTT_PASS, HOME_SSID, HOME_PASS
)
import dht


# Global variables
LATITUDE = {{your latitude here}}
LONGITUDE = {{your longitude here}}
TEN_MINUTES = 600000

# input pins change your pins accordingly
ldr = ADC(Pin(36))
led_wifi = Pin(2, Pin.OUT)
led_iot = Pin(12, Pin.OUT)
i2c = I2C(1, sda=Pin(4), scl=Pin(5))
dht_sensor =dht.DHT11(Pin(33)) # if using DHT22 change to dht.DHT22(Pin())
co_sensor = ADC(Pin(32))


def read_humidity_and_temp():
    "Return the temperature and humidity from the sensor in celsius."
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    hum = dht_sensor.humidity()
    return temp, hum


def read_co():
    """Return the CO concentration in thea ir from sensor in ppm."""
    CO_gas = 0
    for i in range(60):
        analog_value = co_sensor.read_uv()
        voltage = analog_value/10**6
        CO_gas += 595 * pow((5/voltage-1)*(996/850),-2.24)
        time.sleep(1)
    return CO_gas/60 if CO_gas > 0 else 0


async def publish_readings():
    while True:
        global LATITUDE, LONGITUDE, TEN_MINUTES
        try:
            connect_to_wifi()
            temp, humidity = read_humidity_and_temp()
            co = read_co()
            data = {
                    "temp"    : temp,
                    "humidity": humidity,
                    "co": co,
                    "lat": LATITUDE,
                    "lon": LONGITUDE
                    }
            check_mqtt_connection()
            mqtt.publish("b6610545766/project/sensors", json.dumps(data))
            disconnect_mqtt()
            await asyncio.sleep_ms(int(TEN_MINUTES*0.4))
            reconnect_mqtt()
            await asyncio.sleep_ms(int(TEN_MINUTES*0.1))
        except Exception:
            machine.reset()


def connect_to_wifi():
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASS)
        led_wifi.value(1)
        while not wlan.isconnected():
            time.sleep(0.5)
    led_wifi.value(0)
    
    
def reconnect_mqtt():
    mqtt.connect()
    
def disconnect_mqtt():
    mqtt.disconnect()
    

def check_mqtt_connection():
    mqtt.check_msg()


# initialization
led_wifi.value(1)
led_iot.value(1)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("*** Connecting to WiFi...")
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    time.sleep(0.5)
    print("*** Retrying connection...")
print("*** Wifi connected")
led_wifi.value(0)

mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)

print("*** Connecting to MQTT broker...")
mqtt.connect()
print("*** MQTT broker connected")
led_iot.value(0)

# schedule tasks
while True:
    try:
        asyncio.create_task(publish_readings())
        asyncio.run_until_complete()
    except Exception as e:
        machine.reset()
