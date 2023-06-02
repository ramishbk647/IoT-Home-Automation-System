import serial
import json
from datetime import datetime
import paho.mqtt.client as mqtt

ser = serial.Serial('/dev/ttyUSB0', 9600) 

endpoint = "a178yz47tyasj-ats.iot.ap-southeast-2.amazonaws.com"
port = "8883"

cert_file = "a71073859061fe180df925bf887be723590ea6b69988eb5213f480e019f95793-certificate.pem.crt"
private_key_file = "a71073859061fe180df925bf887be723590ea6b69988eb5213f480e019f95793-private.pem.key"
ca_cert_file = "AmazonRootCA1"
topic = "fsensordata"

def on_connect(client, userdate, flags, rc):
	print("Connected to AWS IoT Successfully!")
	client.subscribe(topic)
	
def on_publish(client, userdate, mid):
	print("Message Published!")
	
client = mqtt.Client()

client.tls_set(ca_certs = ca_cert_file, certfile = cert_file, keyfile = private_key_file)
client.on_connect = on_connect
client.on_publish = on_publish

client.connect(endpoint, port, keepalive = 60)

client.loop_start()

temperature = 0
distance = 0
dispensed = ""

while True:
    # Read data from the nodes
    data = ser.readline().decode().strip()
    if data:
        # Split the data into individual values
        node, value = data.split(':')

        # Process the data based on the node
        if node == 'temperature':
            temperature = value
        elif node == 'distance':
            distance = value
        elif node == 'dispensed':
			dispensed = value
			
		msg = {"temperature": temperature, "distance": distance, "dispensed": dispensed}
		client.publish(topic, json.dumps(msg), qos = 1)
		
client.loop_stop()
client.disconnect()
            