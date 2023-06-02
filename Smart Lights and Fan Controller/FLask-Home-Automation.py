
# Import libraries for the Serial, Time and Flask interaction
import mysql.connector
import serial
import time
import boto3
import json
import uuid
from flask import Flask, render_template
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime


app = Flask(__name__)

device = '/dev/ttyUSB0'
arduino = serial.Serial(device,9600)

mydb = mysql.connector.connect(host="localhost",database="home_automation",user="ZashasPI",password="password")
cursor = mydb.cursor()

autobulb = True

sensor_data_batch = []

aws_iot_config = {
    'client_id': 'ZashasRPI',
    'endpoint': 'a178yz47tyasj-ats.iot.ap-southeast-2.amazonaws.com',
    'root_ca_path': '/home/ZashasPI/certs/AmazonRootCA1.pem',
    'private_key_path': '/home/ZashasPI/certs/0d837287713e96474ff64cfb2ede93b8dc0931471348acbba2db7252d4fd3293-private.pem.key',
    'certificate_path': '/home/ZashasPI/certs/0d837287713e96474ff64cfb2ede93b8dc0931471348acbba2db7252d4fd3293-certificate.pem.crt',
    'topic': 'smartroom/data'
}

dynamodb_config = {
    'region_name': 'ap-southeast-2',
    'table_name': 'room_data'
}

dynamodb = boto3.resource('dynamodb',
                          region_name='ap-southeast-2',
                          aws_access_key_id='AKIA4YPVYXHWKNHSR2YX',
                          aws_secret_access_key='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')
table_name = 'room_data'
table = dynamodb.Table(table_name)

# Create an AWS IoT Core MQTT client
client = AWSIoTMQTTClient(aws_iot_config['client_id'])

    # Configure the client
client.configureEndpoint(aws_iot_config['endpoint'], 8883)
client.configureCredentials(aws_iot_config['root_ca_path'], aws_iot_config['private_key_path'], aws_iot_config['certificate_path'])

    # Connect to AWS IoT Core
client.connect()
    
    # Define a Dictionary of pins with the anme of the pin and On/Off state
pins = {
        2: {'name' : 'FAN 1', 'state' : 0},
        3: {'name' : 'FAN 2', 'state' : 0},
        4: {'name' : 'BULB', 'state' : 0},
        5: {'name' : 'DOOR LOCK', 'state' : 0}
    }
    # Activated when the Webpage is loaded/refreshed via URL <WebpageIPAddress>:8080

def generate_unique_id():
    # Generate a unique identifier using UUID
    return str(uuid.uuid4())


def read_arduino_data():
    temperature = 0.0
    sunlight = 0.0
    time = datetime.now()

    while True:
        
        if arduino.in_waiting > 0:
            data =  arduino.readline().decode().rstrip()
            sensor_data = data.split(',')
            if len(sensor_data) == 2:
                sunlight = float(sensor_data[0])
                temperature = float(sensor_data[1])
                insert_data(sunlight, temperature)
                publish_to_aws_iot(sunlight, temperature)
                add_to_dynamodb(sunlight, temperature,time)
                print(sunlight)
        
        

def publish_to_aws_iot(temperature, sunlight):
    

    # Create the payload
    payload = {
        'temperature': temperature,
        'sunlight': sunlight
    }

    # Publish the sensor data to AWS IoT Core
    client.publish(aws_iot_config['topic'], json.dumps(payload), 0)

    # Disconnect from AWS IoT Core
    

def add_to_dynamodb(sunlight, temperature, time):
    
    
    item = {
        'id': generate_unique_id(),
        'temperature': str(temperature),
        'sunlight': str(sunlight),
        'timestamp': str(time)
    }

    # Add the item to the batch
    sensor_data_batch.append(item)

    # Check if the batch size exceeds a certain threshold (e.g., 10 items)
    if len(sensor_data_batch) >= 10:
        # Put the batch of items into DynamoDB table
        with table.batch_writer() as batch:
            for item in sensor_data_batch:
                batch.put_item(Item=item)

        # Clear the batch after sending
        sensor_data_batch.clear()
    
            
@app.route("/")
def index():
    # Read the status of pins from Dictionary and put it into the template
    templateData = {
        'pins' : pins
    }
    
    mydb.reconnect()
    cursor = mydb.cursor()
    query = "SELECT sunlight, temperature FROM sensordata ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    data = cursor.fetchone()

    # Check if data is available
    if data:
        sunlight, temperature = data
    else:
        temperature = 'N/A'
        sunlight = 'N/A'
        
    # Update the Webpage with the template's contents
    return render_template('index.html',**templateData,sunlight = sunlight, temperature = temperature)
    # Activated when the URL <WebpageIPAddress>:8080/action<something> is passed
    
@app.route("/<action>")
def action(action):
    # See if the action matches. If yes, write a serial message to the Microcontroller.
    # The Microcontroller needs to receive and interpret the message.
    # Don't forget to update our Dictionary values too, so the refresh works properly.
    if action == 'action1':
        ser.write(b"1")
        pins[2]['state'] = 1
    if action == 'action2':
        ser.write(b"2")
        pins[2]['state'] = 0
    if action == 'action3':
        ser.write(b"3")
        pins[3]['state'] = 1
    if action == 'action4':
        ser.write(b"4")
        pins[3]['state'] = 0
    if action == 'action5':
        ser.write(b"5")
        pins[4]['state'] = 1
    if action == 'action6':
        ser.write(b"6")
        pins[4]['state'] = 0
    if action == 'action7':
        ser.write(b"7")
        pins[5]['state'] = 1
    if action == 'action8':
        ser.write(b"8")
        pins[5]['state'] = 0
    if action == 'action9':
        ser.write(b"9")
        autobulb = True
        insert_bulbdata(autobulb)
    if action == 'action10':
        ser.write(b"10")
        autobulb = False
        insert_bulbdata(autobulb)
    # Like before, read the contents of the Dictionary, update the template,
    # then update the Webpage based on the template.
    templateData = {
        'pins' : pins
    }
    return render_template('index.html',**templateData)
# Activated when the URL <WebpageIPAddress>:8080/<device number>/<on/off> is passed.
@app.route("/<changePin>/<toggle>")
def toggle_function(changePin,toggle):
    # Originally, changePin value is in text. Need to convert it into Integer.
    changePin = int(changePin)
    # Get the real Device Name from the Dictionary. Need this as a label later.
    deviceName = pins[changePin]['name']
    # Check to see if we want to toggle the Device on or off.
    # Then send the appropriate Serial Message to the Microcontroller.
    if toggle == "on":
        if changePin == 2:
            ser.write(b"1")
            pins[changePin]['state'] = 1
        if changePin == 3:
            ser.write(b"3")
            pins[changePin]['state'] = 1
        if changePin == 4:
            ser.write(b"5")
            pins[changePin]['state'] = 1
        if changePin == 5:
            ser.write(b"7")
            pins[changePin]['state'] = 1
            # Then write a label message saying the Device is ON.
            message = "Turned " + deviceName + "on."
    if toggle == "off":
        if changePin == 2:
            ser.write(b"2")
            pins[changePin]['state'] = 0
        if changePin == 3:
            ser.write(b"4")
            pins[changePin]['state'] = 0
        if changePin == 4:
            ser.write(b"6")
            pins[changePin]['state'] = 0
        if changePin == 5:
            ser.write(b"8")
            pins[changePin]['state'] = 0
            # Then write a label message saying the Device is ON.
            message = "Turned " + deviceName + "off."
            # Like before, read the contents of the Dictionary, update the template,
            # then update the Webpage based on the template.
    templateData = {
        'pins' : pins
    }
    return render_template('index.html',**templateData)

# Route to receive sensor data from Arduino
@app.route('/receive', methods=['POST'])
def receive_data():
    receive_sensor_data()
    return 'Success'

def insert_data(sunlight, temperature):
    
    query = "INSERT INTO sensordata (sunlight, temperature) VALUES (%s, %s)"
    values = (sunlight, temperature)
    cursor.execute(query, values)
    mydb.commit()

def insert_bulbdata(autobulb):
    
    query = "INSERT INTO bulbtable (bulb_status) VALUES (%s)"
    values = (int(autobulb),)
    print(query)
    cursor.execute(query, values)
    mydb.commit()
# Finally, start the Flask micro-web-framework server,
# and establish the Serial Messaging connection to the Microcontroller.
if __name__ == "__main__":
    
    import threading
    
    t = threading.Thread(target=read_arduino_data)
    t.start()
    
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    app.run(host='0.0.0.0',port=8080,debug=False)
