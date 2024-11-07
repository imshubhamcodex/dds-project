from config import dds_config
import rti.connextdds as dds
from time import sleep

participant = dds_config.create_participant()
publisher = dds.Publisher(participant)

# Create a topic and DataWriter for `inflow_velocity`
topic = dds.Topic(participant, "inflow_velocity", dds_config.FloatWrapper)
writer = dds.DataWriter(publisher, topic)

# Sensor data 
inflow_velocity_values = [
    8.0, 9.0, 9.5, 9.8, 9.0, 8.5, 8.0, 8.8,       
    9.9, 9.0, 8.9, 8.5,9.0, 8.5, 8.0, 8.8,
    9.9, 9.5, 9.0, 8.5,9.0, 8.5, 8.0, 8.8,
    9.0, 8.5, 8.0, 8.8,9.0, 8.5, 8.0, 8.8,
    11.0, 11.5, 12.0, 11.4, 11.0, 11.5, 12.0, 11.4, 
    9.3, 9.5, 8.3, 8.8, 9.0, 8.5, 8.0, 8.8,
]

msg_counter = 0
while True:
    message = dds_config.FloatWrapper(value=inflow_velocity_values[msg_counter % len(inflow_velocity_values)])
    msg_counter += 1
    writer.write(message)
    print(f"{msg_counter}. inflow_velocity published: {message.value}")
    sleep(2)
