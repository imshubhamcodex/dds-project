from config import dds_config
import rti.connextdds as dds
from time import sleep
from datetime import datetime

participant = dds_config.create_participant()
publisher = dds.Publisher(participant)

# Create a topic and DataWriter for `water_level`
topic = dds.Topic(participant, "water_level", dds_config.FloatWrapper)
writer = dds.DataWriter(publisher, topic)

# Sensor data
water_level_values = [
    90.0, 95.0, 99.0, 99.9, 97.0, 96.0, 95.0, 98.2, 
    101.0, 102.0, 103.0, 100.1, 101.0, 102.0, 103.0, 100.1,
    97.0, 96.0, 95.0, 98.2,  97.0, 96.0, 95.0, 98.2,    
    97.0, 96.0, 95.0, 99,8, 97.0, 96.0, 95.0, 98.2,   
    98.0, 97.5, 95.0, 91,9, 97.0, 96.0, 95.0, 98.2, 
    92.0, 93.0, 97.0, 92.9, 97.0, 96.0, 95.0, 98.2, 
]

msg_counter = 0
while True:
    message = dds_config.FloatWrapper(value=water_level_values[msg_counter % len(water_level_values)])
    msg_counter += 1
    writer.write(message)
    # print(f"{msg_counter}. water_level published: {message.value}")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Sensor: Ultrasonic | Reads: Water Level | Location: Spillway | Value: {message.value} meters | Status: Live |")
    
    sleep(2)
