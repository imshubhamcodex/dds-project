from config import dds_config
import rti.connextdds as dds
from time import sleep

participant = dds_config.create_participant()
publisher = dds.Publisher(participant)

# Create a topic and DataWriter for `water_level`
topic = dds.Topic(participant, "water_level", dds_config.FloatWrapper)
writer = dds.DataWriter(publisher, topic)

# Sensor data
water_level_values = [
    90.0, 95.0, 99.0, 99.9,
    101.0, 102.0, 103.0, 100.1,
    97.0, 96.0, 95.0, 98.2,     
    97.0, 96.0, 95.0, 99,8,   
    98.0, 97.5, 95.0, 91,9,
    92.0, 93.0, 97.0, 92.9,
]

msg_counter = 0
while True:
    message = dds_config.FloatWrapper(value=water_level_values[msg_counter % len(water_level_values)])
    msg_counter += 1
    writer.write(message)
    print(f"{msg_counter}. water_level published: {message.value}")
    sleep(1)
