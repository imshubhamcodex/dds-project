# pip install rti.connext
from config import dds_config
import rti.connextdds as dds
from time import sleep
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
        print(f"{msg_counter}. No Command received")
    for sample in samples:
        data = sample.data
        print(f"{msg_counter}. Received Command: {data.content}")
        upload_data()
    sleep(0.4)