from config import dds_config
from datetime import datetime
import rti.connextdds as dds
from datetime import datetime
import json
from config.firebase_firestore_config import is_mode_MANUAL

participant = dds_config.create_participant()
publisher = dds.Publisher(participant)

# Create a topic and DataWriter for `actuation_command`
topic = dds.Topic(participant, "actuation_command", dds_config.StringWrapper)
writer = dds.DataWriter(publisher, topic)

previous_command = None
current_door_height = 0
data_collection_list = []

# Publish `actuation_command` data
def send_command(data_collection, action_type, door_open_height, action_remark):
    global data_collection_list
    
    # Adding action fields
    data_collection['action_type'] = action_type
    data_collection['door_open_height'] = door_open_height
    data_collection['action_remark'] = action_remark
    data_collection['timestamp'] = datetime.now().strftime("%d:%m:%Y %H:%M:%S")
    data_collection_list.append(data_collection)
    
    data_dumping(data_collection_list, "publishers-actuation-data.json")
    message = dds_config.StringWrapper(content=f"{action_type}-{door_open_height}-{action_remark}")
    writer.write(message)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Identity: Data Analyzer | Performs: Data Analysis | Location: Control Room | Status: Data Analysis Compelete | Action: Instruction Relayed |")
    print(" ")
        


def data_dumping(data, file_name):
    with open("./data/" + file_name, "w") as file:
        json.dump(data, file)

# Perform analytics
def perform_analytics(data_collection):
    global previous_command
    global current_door_height
    
    if not data_collection or len(data_collection.keys()) < 6:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Identity: Data Analyzer | Performs: Data Analysis | Location: Control Room | Status: Invalid or Corrupt Data Received | Action: Data Purged |")
        print(" ")
        return
    
    if is_mode_MANUAL():
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Identity: Data Analyzer | Performs: Data Analysis | Location: Control Room | Status: Operation Mode 'MANUAL' | Action: Analysis Not Performed |")
        print(" ")
        return
    
    # Default action details
    door_open_height = 0
    action_remark = None

    # Thresholds for individual conditions
    WATER_LEVEL_THRESHOLD = 100.0
    WATER_PRESSURE_THRESHOLD = 75.0
    FO_HEIGHT_THRESHOLD = 20.0
    FO_WIDTH_THRESHOLD = 15.0
    INFLOW_VELOCITY_THRESHOLD = 10.0
    EMERGENCY_STATUS_ALERT = "ALERT"

    # Determine action based on conditions
    if data_collection.get("emergency_status") == EMERGENCY_STATUS_ALERT:
        door_open_height = 100
        action_remark = "Emergency Detected!"
    elif data_collection.get("water_level", 0) > WATER_LEVEL_THRESHOLD:
        door_open_height = 75
        action_remark = "High Water Level Detected."
    elif data_collection.get("water_pressure", 0) > WATER_PRESSURE_THRESHOLD:
        door_open_height = 50
        action_remark = "High Water Pressure Detected."
    elif data_collection.get("fo_height", 0) > FO_HEIGHT_THRESHOLD:
        door_open_height = 0
        action_remark = "Long Height Floating Object Detected."
    elif data_collection.get("fo_width", 0) > FO_WIDTH_THRESHOLD:
        door_open_height = 0
        action_remark = "Large Width Floating Object Detected."
    elif data_collection.get("inflow_velocity", 0) > INFLOW_VELOCITY_THRESHOLD:
        door_open_height = 25
        action_remark = "High Inflow Velocity Detected."

    # Build current command and compare to previous command
    current_command = f"{door_open_height}-{action_remark}"
    
    # Check if current command differs from the previous command
    if current_command != previous_command and action_remark != None:
        if current_door_height > door_open_height:
            action_type = "CLOSE"
        elif current_door_height < door_open_height:
            action_type = "OPEN"
        else:
            action_type = "NONE"
            action_remark = "No Change Requried"
            
        previous_command = current_command
        current_door_height = door_open_height
        
        send_command(data_collection, action_type, door_open_height, action_remark)
    else:
        if action_remark != None: # Eliminating initial condition
            action_type = "NONE"
            action_remark = "No Change Requried"
            
            previous_command = current_command
            send_command(data_collection, action_type, door_open_height, action_remark)
            
