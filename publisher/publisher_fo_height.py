from config import dds_config
import rti.connextdds as dds
from time import sleep
from datetime import datetime

participant = dds_config.create_participant()
publisher = dds.Publisher(participant)

# Create a topic and DataWriter for `fo_height`
topic = dds.Topic(participant, "fo_height", dds_config.FloatWrapper)
writer = dds.DataWriter(publisher, topic)

# Sensor data 
fo_height_values = [
    18.0, 19.0, 19.5, 19.9, 19.0, 18.5, 18.0, 18.8,  
    19.9, 20.0, 19.6, 20.0,18.0, 19.0, 19.5, 19.9,
    19.0, 18.5, 18.0, 18.8, 19.0, 18.5, 18.0, 18.8,    
    19.0, 18.5, 18.0, 19.1,19.0, 18.5, 18.0, 18.8, 
    20.0, 19.5, 19.0, 18.9,19.0, 18.5, 18.0, 18.8, 
    21.0, 21.5, 22.0, 21,2, 21.5, 22.0, 21,2,21,2, 21.5, 22.0, 21,2     
]

msg_counter = 0
while True: 
    message = dds_config.FloatWrapper(value=fo_height_values[msg_counter % len(fo_height_values)]) 
    msg_counter += 1 
    writer.write(message)
    # print(f"{msg_counter}. fo_height published: {message.value}")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Sensor: LIDAR | Reads: Floating Object Height | Location: Reservoir Surface | Value: {message.value} meters | Status: Live |")
    
    sleep(2)
