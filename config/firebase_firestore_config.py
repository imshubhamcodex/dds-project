import firebase_admin
from firebase_admin import credentials, firestore
from time import sleep
import json

cred = credentials.Certificate("db_private_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection("dam_data").document("data")
doc_mode_ref = db.collection("mode").document("info")


def set_mode(mode):
    doc_mode_ref.set({"mode": mode})
    
def is_mode_MANUAL():
     doc_mode = doc_mode_ref.get().to_dict()
     return doc_mode['mode'] == "MANUAL"

def update_manual_data(manual_data):
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            data['entries'].append(manual_data)
            doc_ref.set(data) 
            print("Manual data set")
        else:
            print("No data found in DB")   
    

def get_unique_local_data(local_data, db_data):
    # Extract all timestamps from db_data for quick lookup
    db_timestamps = {obj["timestamp"] for obj in db_data}
    # Filter local_data to include only objects with timestamps not in db_timestamps
    unique_local_data = [obj for obj in local_data if obj["timestamp"] not in db_timestamps]
    return unique_local_data


def upload_data():
    file_path = "./data/publishers-actuation-data.json"
    doc = doc_ref.get()
    
    if doc.exists and len(doc.to_dict()) > 0:
        db_data = doc.to_dict()
        db_data = db_data['entries']
        try:
            with open(file_path, "r") as file:
                local_data = json.load(file)
                new_obj_arr = get_unique_local_data(local_data, db_data)
                if local_data:
                    doc_data = {"entries": db_data + new_obj_arr}
                    doc_ref.set(doc_data)
                    print("Data uploaded")
        except json.JSONDecodeError:
                print("JSON file fetch Error")
                sleep(0.5)
                upload_data()
    else:
        upload_local_data()
                
def upload_local_data():
    file_path = "./data/publishers-actuation-data.json"
    try:
        with open(file_path, "r") as file:
            local_data = json.load(file)
            if local_data:
                doc_data = {"entries": local_data}
                doc_ref.set(doc_data)
                print("Local Data uploaded")
    except json.JSONDecodeError:
            print("JSON file fetch Error")
            sleep(0.5)
            upload_local_data()
    

def fetch_data():
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()

        formatted_data = {
            "Date Time": [],
            "Water Level(m)": [],
            "Water Pressure(Pa)": [],
            "Inflow Velocity(m/s)": [],
            "FO Height(m)": [],
            "FO Width(m)": [],
            "Emergency Status": [],
            "Action": [],
            "Door Height(%)": [],
            "Remarks": []
        }
        
        if len(data) == 0:
            return formatted_data

        # Populate the formatted data structure
        for entry in data['entries']:
            formatted_data["Date Time"].append(entry.get('timestamp', ''))
            formatted_data["Water Level(m)"].append(str(entry.get('water_level', '')))
            formatted_data["Water Pressure(Pa)"].append(str(entry.get('water_pressure', '')))
            formatted_data["Inflow Velocity(m/s)"].append(str(entry.get('inflow_velocity', '')))
            formatted_data["FO Height(m)"].append(str(entry.get('fo_height', '')))
            formatted_data["FO Width(m)"].append(str(entry.get('fo_width', '')))
            formatted_data["Emergency Status"].append(entry.get('emergency_status', ''))
            formatted_data["Remarks"].append(entry.get('action_remark', ''))
            formatted_data["Action"].append(entry.get('action_type', ''))
            formatted_data["Door Height(%)"].append(float(entry.get('door_open_height', '')))

            
        return formatted_data
    
    else:
        print("No such document!")   

