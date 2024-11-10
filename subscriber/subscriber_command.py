# pip install rti.connext
from config import dds_config
import rti.connextdds as dds
from time import sleep
from datetime import datetime
from config.firebase_firestore_config import upload_data

participant = dds_config.create_participant()
topic = dds.Topic(participant, "actuation_command", dds_config.StringWrapper)

subscriber = dds.Subscriber(participant)
reader = dds.DataReader(subscriber, topic)

msg_counter = 0
while True:
    samples = reader.take()
    msg_counter += 1
    
    if len(samples) == 0:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Identity: Actuation Controller | Location: Across Reservoir | Status: Waiting For Instruction | Action: None |")
         
    for sample in samples:
        data = sample.data
        action = data.content.split("-")[0] + " Height(meters) "+ data.content.split("-")[1] 
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(" ")
        print(f"[{timestamp}] Identity: Actuation Controller | Location: Across Reservoir | Status: Instruction Received | Action: {action} |")
        print(" ")
        upload_data()
    sleep(0.4)