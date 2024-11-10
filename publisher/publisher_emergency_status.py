from config import dds_config
import rti.connextdds as dds
from time import sleep
from datetime import datetime

participant = dds_config.create_participant()
publisher = dds.Publisher(participant)

# Create a topic and DataWriter for `emergency_status`
topic = dds.Topic(participant, "emergency_status", dds_config.StringWrapper)
writer = dds.DataWriter(publisher, topic)

# Sensor data 
emergency_status_values = [
    "ALERT", "ALERT", "ALERT", "ALERT", "ALERT", "ALERT",
    "NORMAL", "NORMAL", "NORMAL", "NORMAL","NORMAL", "NORMAL",
    "NORMAL", "NORMAL", "NORMAL", "NORMAL", "NORMAL", "NORMAL",
    "NORMAL", "NORMAL", "NORMAL" ,"NORMAL","NORMAL", "NORMAL",
    "NORMAL", "NORMAL", "NORMAL" , "NORMAL","NORMAL", "NORMAL",
    "NORMAL", "NORMAL", "NORMAL" , "NORMAL","NORMAL", "NORMAL"
]

msg_counter = 0
while True:
    message = dds_config.StringWrapper(content=emergency_status_values[msg_counter % len(emergency_status_values)])
    msg_counter += 1
    writer.write(message)
    # print(f"{msg_counter}. emergency_status published: {message.content}")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Sensor: Emergrncy Detector | Reads: Emergency Status | Location: Control Room | Value: {message.content} | Status: Live |")
    
    sleep(2)
