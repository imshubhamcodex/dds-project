from config import dds_config
import rti.connextdds as dds
from time import sleep
from datetime import datetime

participant = dds_config.create_participant()
publisher = dds.Publisher(participant)

# Create a topic and DataWriter for `water_pressure`
topic = dds.Topic(participant, "water_pressure", dds_config.FloatWrapper)
writer = dds.DataWriter(publisher, topic)

# Sensor data
water_pressure_values = [
    70.0, 72.0, 74.0, 73.2,  74.0, 71.0, 72.0, 73.2,   
    71.0, 73.3, 72.0, 71.1,  74.0, 71.0, 72.0, 73.2,       
    76.0, 77.0, 78.0, 75.1, 76.0, 77.0, 78.0, 75.1,
    74.0, 71.0, 72.0, 73.2, 74.0, 71.0, 72.0, 73.2,
    73.0, 72.5, 71.0, 75.0, 74.0, 71.0, 72.0, 73.2,
    74.0, 73.5, 71.1, 72.0 , 74.0, 71.0, 72.0, 73.2,  
]

msg_counter = 0
while True:
    message = dds_config.FloatWrapper(value=water_pressure_values[msg_counter % len(water_pressure_values)]) 
    msg_counter += 1
    writer.write(message)
    # print(f"{msg_counter}. water_pressure published: {message.value}")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Sensor: Hydrostatic | Reads: Water Pressure | Location: Reservoir Walls | Value: {message.value} Pa | Status: Live |")
    
    sleep(2)
