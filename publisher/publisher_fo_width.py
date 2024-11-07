from config import dds_config
import rti.connextdds as dds
from time import sleep

participant = dds_config.create_participant()
publisher = dds.Publisher(participant)

# Create a topic and DataWriter for `fo_width`
topic = dds.Topic(participant, "fo_width", dds_config.FloatWrapper)
writer = dds.DataWriter(publisher, topic)

# Sensor data 
fo_width_values = [
    13.0, 14.0, 14.5, 15.0,     
    13.1, 14.1, 13.3, 14.4,     
    14.5, 14.0, 13.5, 14.4, 
    16.0, 16.5, 17.0, 18.1,   
    13.0, 14.5, 12.5, 12.2,    
    14.0, 13.5, 13.0, 14.4,
]


msg_counter = 0
while True:
    message = dds_config.FloatWrapper(value=fo_width_values[msg_counter % len(fo_width_values)])
    msg_counter += 1
    writer.write(message)
    print(f"{msg_counter}. fo_width published: {message.value}")
    sleep(1)