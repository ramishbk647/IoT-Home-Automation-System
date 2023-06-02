import serial
import mysql.connector
from datetime import datetime

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='smartpetfeeder'
)
cursor = conn.cursor()

# Initialize serial communication with the nodes
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace '/dev/ttyUSB0' with your serial port

while True:
    # Read data from the nodes
    data = ser.readline().decode().strip()
    if data:
        # Split the data into individual values
        node, value = data.split(':')

        # Process the data based on the node
        if node == 'temperature':
            # Save temperature data to the database
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO datasaver (timestamp, temperature) VALUES (%s, %s)", (timestamp, value))
            conn.commit()
        elif node == 'distance':
            # Save ultrasonic sensor data to the database
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO datasaver (timestamp, fooddispense) VALUES (%s, %s)", (timestamp, value))
            conn.commit()
        elif node == 'dispensed':
            # Save servo motor data to the database
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO datasaver (timestamp, servo) VALUES (%s, %s)", (timestamp, value))
            conn.commit()
