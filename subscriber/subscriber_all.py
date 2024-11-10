# pip install rti.connext
import rti.connextdds as dds
from publisher.publisher_local_analytics  import perform_analytics
from config import dds_config   
from time import sleep
from datetime import datetime

participant = dds_config.create_participant()

# Define topics and types
topics = {
    "water_level": dds_config.FloatWrapper,
    "water_pressure": dds_config.FloatWrapper,
    "fo_height": dds_config.FloatWrapper,
    "fo_width": dds_config.FloatWrapper,
    "inflow_velocity": dds_config.FloatWrapper,
    "emergency_status": dds_config.StringWrapper,
}


subscriber = dds.Subscriber(participant)

# Create a DataReader for each topic
readers = {}
for topic_name, topic_type in topics.items():
    topic = dds.Topic(participant, topic_name, topic_type)
    readers[topic_name] = dds.DataReader(subscriber, topic)


msg_counter = 0
while True:
    data_collection = {}
    for topic_name, reader in readers.items():
        samples = reader.take()
        if not samples:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Identity: Central Data Reader | Reads: All Sensor Data | Location: Control Room | Status: Waiting For Data |")
            continue
        
        msg_counter += 1 
        for sample in samples:
            data = sample.data
            if hasattr(data, "value"):
                data_collection[topic_name] = data.value
            elif hasattr(data, "content"):
                data_collection[topic_name] = data.content
            
    # Invoking analytics with current data
    print(" ")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Identity: Central Data Reader | Performs: Data Collection | Location: Control Room | Status: Data Received | Action: Forwarded For Analysis |")
    perform_analytics(data_collection)
  
    sleep(2.2) 
    
