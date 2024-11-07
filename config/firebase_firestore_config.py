import firebase_admin
from firebase_admin import credentials, firestore
from time import sleep
import json

cred = credentials.Certificate("db_private_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection("dam_data").document("data")

def upload_data():
    file_path = "./data/publishers-actuation-data.json"
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            if data:
                doc_data = {"entries": data}
                doc_ref.set(doc_data)
                print("Data uploaded")
    except json.JSONDecodeError:
            print("JSON file fetch Error")
            sleep(0.5)
            upload_data()

def fetch_data():
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()

        formatted_data = {
            "Date Time": [],
            "Water Level(m)": [],
            "Water Pressure(Pa)": [],
            "Initial Velocity(m/s)": [],
            "FO Height(m)": [],
            "FO Width(m)": [],
            "Emergency Status": [],
            "Action": [],
            "Door Height(%)": [],
            "Remarks": []
        }

        # Populate the formatted data structure
        for entry in data['entries']:
            formatted_data["Date Time"].append(entry.get('timestamp', ''))
            formatted_data["Water Level(m)"].append(str(entry.get('water_level', '')))
            formatted_data["Water Pressure(Pa)"].append(str(entry.get('water_pressure', '')))
            formatted_data["Initial Velocity(m/s)"].append(str(entry.get('inflow_velocity', '')))
            formatted_data["FO Height(m)"].append(str(entry.get('fo_height', '')))
            formatted_data["FO Width(m)"].append(str(entry.get('fo_width', '')))
            formatted_data["Emergency Status"].append(entry.get('emergency_status', ''))
            formatted_data["Remarks"].append(entry.get('action_remark', ''))
            formatted_data["Action"].append(entry.get('action_type', ''))
            formatted_data["Door Height(%)"].append(entry.get('door_open_height', ''))

            
        return formatted_data
    
    else:
        print("No such document!")   

