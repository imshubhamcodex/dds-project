from config import dds_config
import rti.connextdds as dds
from time import sleep
from datetime import datetime

participant = dds_config.create_participant()
publisher = dds.Publisher(participant)

# Create a topic and DataWriter for `fo_width`
topic = dds.Topic(participant, "fo_width", dds_config.FloatWrapper)
writer = dds.DataWriter(publisher, topic)

# Sensor data 
fo_width_values = [
    13.0, 14.0, 14.5, 15.0, 13.0, 14.0, 14.5, 15.0, 
    13.1, 14.1, 13.3, 14.4, 13.0, 14.0, 14.5, 15.0,     
    14.5, 14.0, 13.5, 14.4, 13.0, 14.0, 14.5, 15.0, 
    16.0, 16.5, 17.0, 18.1, 16.0, 16.5, 17.0, 18.1,   
    13.0, 14.5, 12.5, 12.2, 13.0, 14.0, 14.5, 15.0, 
    14.0, 13.5, 13.0, 14.4, 13.0, 14.0, 14.5, 15.0, 
]

msg_counter = 0
while True:
    message = dds_config.FloatWrapper(value=fo_width_values[msg_counter % len(fo_width_values)])
    msg_counter += 1
    writer.write(message)
    # print(f"{msg_counter}. fo_width published: {message.value}")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Sensor: LIDAR | Reads: Floating Object Width | Location: Reservoir Surface | Value: {message.value} meters | Status: Live |")
    
    sleep(2)
