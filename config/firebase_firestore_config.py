import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate("db_private_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection("dam_data").document("data")

def upload_data():
    file_path = "./data/publishers-actuation-data.json"
    with open(file_path, "r") as file:
        data = json.load(file)
        if data:
            doc_data = {"entries": data}
            doc_ref.set(doc_data)
            print("Data uploaded")

def fetch_data():
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()

        formatted_data = {
            "Date&Time(dd:mm:yyyyThh:mm:ss)": [],
            "Publisher - Water Level(m)": [],
            "Publisher - Water Pressure(Pa)": [],
            "Publisher - Initial Velocity(m/s)": [],
            "Publisher - FO Height(m)": [],
            "Publisher - FO Width(m)": [],
            "Publisher - Emergency Status": [],
            "Action": [],
            "By %": [],
            "Remarks": []
        }

        # Populate the formatted data structure
        for entry in data['entries']:
            formatted_data["Date&Time(dd:mm:yyyyThh:mm:ss)"].append(entry.get('timestamp', ''))
            formatted_data["Publisher - Water Level(m)"].append(str(entry.get('water_level', '')))
            formatted_data["Publisher - Water Pressure(Pa)"].append(str(entry.get('water_pressure', '')))
            formatted_data["Publisher - Initial Velocity(m/s)"].append(str(entry.get('inflow_velocity', '')))
            formatted_data["Publisher - FO Height(m)"].append(str(entry.get('fo_height', '')))
            formatted_data["Publisher - FO Width(m)"].append(str(entry.get('fo_width', '')))
            formatted_data["Publisher - Emergency Status"].append(entry.get('emergency_status', ''))
            formatted_data["Remarks"].append(entry.get('action_remark', ''))
            formatted_data["Action"].append(entry.get('action_type', ''))
            formatted_data["By %"].append(entry.get('adjustment_percentage', ''))

            
        return formatted_data
    
    else:
        print("No such document!")   

