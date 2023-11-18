import machine
import dht
from simple import MQTTClient
import network
import time

# WiFi settings
WIFI_SSID = 'WIFI SSID'
WIFI_PASSWORD = 'WIFI PASSWORD'

# MQTT settings
MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'pico_sensor'
MQTT_TOPIC = b'sensor_data'

# DHT11 sensor setup
dht_pin = machine.Pin(16, machine.Pin.IN)  # Assuming DHT11 is connected to GPIO pin 16
dht_sensor = dht.DHT11(dht_pin)

# Connect to Wi-Fi
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    print('Connecting to Wi-Fi...')
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)

# Connect to MQTT broker
def connect_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    return client

def read_sensor_data():
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    return temperature

connect_wifi()
mqtt_client = connect_mqtt()

while True:
    temperature = read_sensor_data()
    mqtt_client.publish(MQTT_TOPIC, str(temperature))
    print('Data sent!',temperature)
    time.sleep(60)  # Send data every 60 seconds

