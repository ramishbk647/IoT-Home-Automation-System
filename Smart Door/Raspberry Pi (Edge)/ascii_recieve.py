import serial
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import time

# Function to insert a row into the table
def insert_row(node_id, distance, motion_sensor, obj, door_status):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='sensor_data',
            user='root',
            password='root'
        )

        # Create a cursor object to execute queries
        cursor = connection.cursor()

        # Generate the timestamp automatically
        timestamp = datetime.now()

        # Construct the INSERT query with placeholders for the values
        insert_query = "INSERT INTO data_sensor (node_id, timestamp, distance, motion_sensor, object, door_status) VALUES (%s, %s, %s, %s, %s, %s)"

        # Execute the query with the provided values
        cursor.execute(insert_query, (node_id, timestamp, distance, motion_sensor, obj, door_status))

        # Commit the changes to the database
        connection.commit()

        print("Row inserted successfully!")

    except Error as e:
        print("Error while connecting to MySQL:", e)

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()

ser = serial.Serial('/dev/ttyACM1', 9600)

distance = 0
motion_sensor = 100
object_ = '-'
door_status = '-'

while True:
    res = ser.readline().decode().strip()
    if res > '1' and len(res) <= 4:
            distance = int(res)
    elif res == '1' or res == '0':
        motion_sensor = int(res)
    elif len(res) < 6:
        door_status = res
    else:
        object_ = res
   
    print('Object at distance ', distance)
    print('Motion Status: ', motion_sensor)
    print('SUMMARY')
    print('\t',object_)
    print('\t',door_status)
    
    insert_row(1,distance,motion_sensor,object_,door_status)
    
    time.sleep(1)