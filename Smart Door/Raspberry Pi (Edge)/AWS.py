import time
import json
import serial
import paho.mqtt.client as mqtt

ser = serial.Serial('/dev/ttyACM0', 9600)

distance = 0
motion_sensor = 100
object_ = '-'
door_status = '-'

# AWS IoT Core endpoint and port
broker_endpoint = "a178yz47tyasj-ats.iot.ap-southeast-2.amazonaws.com"
broker_port = 8883

# Paths to your AWS IoT certificates and private key
cert_file = "./ccee8cd1cb4938254e51b688df5eab18e0580add04aa0706382a59b7ecb4fa91-certificate.pem.crt"
private_key_file = "./ccee8cd1cb4938254e51b688df5eab18e0580add04aa0706382a59b7ecb4fa91-private.pem.key"
ca_cert_file = "./AmazonRootCA1.pem"

# MQTT topic to publish to
topic = "mqtt-data"

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT")
    client.subscribe(topic)

# Callback function for MQTT publish
def on_publish(client, userdata, mid):
    print("Message published")

# Create MQTT client instance
client = mqtt.Client()

# Set MQTT client parameters
client.tls_set(ca_certs=ca_cert_file, certfile=cert_file, keyfile=private_key_file)
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect(broker_endpoint, broker_port, keepalive=60)

# Wait for MQTT connection to be established
client.loop_start()
while not client.is_connected:
    time.sleep(1)

while True:
    res = ser.readline().decode().strip()
    if res > '1' and len(res) <= 4:
            distance = res
    elif res == '1' or res == '0':
        motion_sensor = int(res)
    elif len(res) < 6:
        door_status = res
    else:
        object_ = res
    # Publish messages
    message = {"distance": distance, "pir-sensor": motion_sensor}
    client.publish(topic, json.dumps(message), qos=1)

# Disconnect from the MQTT broker
client.loop_stop()
client.disconnect()
