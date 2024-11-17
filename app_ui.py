from taipy import Gui
from datetime import datetime
import plotly.graph_objects as go
from config.firebase_firestore_config import fetch_data, set_mode, update_manual_data
from dotenv import load_dotenv
import os

# Dialog state vars
dialog_is_visible = True
passcode = None
verified_user = False

# Control state vars
mode_value = "AUTO"
action_type = "OPEN"
door_height = 0
show_ele = True
show_door_height = False
active_btn = False 
input_val_msg =""

# Chart and Table vars
chart_fig = None
table_data = None
door_open_height = None
timestamp = None
data = None

# Table data manipulation
def get_table_data(data):
    data_key = data.keys()
    data_dict = {}
    for key in data_key:
        rev_val = data.get(key)
        data_dict[key] = rev_val[::-1]
    return data_dict

    
page_0 ="""
<|{dialog_is_visible}|dialog|title=Enter the Passcode|
<|{passcode}|number|on_change=verify_passcode|>
|>
"""

page_1 = """
<|layout|columns=1 1 1|
#
<|part|id=nav-bar|
<|navbar|>
|>
#
<br/>
|>
# 
<|part|render={verified_user}
<|chart|figure={chart_fig}|>
|>
"""

page_2 = """
<|layout|columns=1 1 1|
#
<|part|id=nav-bar|
<|navbar|>
|>
#
|>
<br/>
# 
<|{table_data}|table|>
"""

page_3 = """
<|layout|columns=1 1 1|
#
<|part|id=nav-bar|
<|navbar|>
|>
#
|>
# 
# 
<br />
<br />
<|layout|columns=1 1 1|
#
<|layout|
<|part|
<|{mode_value}|selector|lov=MANUAL;AUTO;|dropdown|label=Operation Mode|on_change=mode_toggle|>
|>
<|part|render={show_ele}
<|{door_height}|input|label=Door Height(%)|active={show_door_height}|on_change=validate_input|>
<|{input_val_msg}|text|id=text_msg|>
|>
<|part|render={show_ele}
<|execute|button|on_action=execute|id=exe-btn|active={active_btn}|>
|>
|>
#
|>
"""

   
# Global on_navigate
def on_navigate(state, page_name):
    if verified_user:
        page_refresh(state)
        
    return page_name

# Local on_change
def verify_passcode(state, id):  
    if state.passcode:
        state.passcode = int(state.passcode)

        if state.passcode == int(os.getenv('passcode')):
            state.dialog_is_visible = False
            state.verified_user = True
            page_refresh(state)


# Local on_change
def validate_input(state, id):
    input_door_height = str(state.door_height)
    try:
        height = float(input_door_height)
        if height < 0 or height > 100:
            state.input_val_msg = "Must in between 0 and 100."
            state.active_btn = False
        else:
            state.input_val_msg = ""
            state.active_btn = True
    except ValueError:
        state.input_val_msg = "Must be a numeric value."
        state.active_btn = False

# Local on_change
def mode_toggle(state, id):
    if state.mode_value == "MANUAL":
        state.show_door_height = True
        state.active_btn = True
    else:
        state.show_door_height = False
        state.door_height = 0
        state.active_btn = False
        execute(state, id)


# Utility function        
def page_refresh(state):
    new_data = fetch_data()
    state.data = new_data
    state.table_data = get_table_data(new_data)
    state.door_open_height = new_data.get('Door Height(%)')
    state.timestamp = new_data.get('Date Time')
    state.chart_fig = go.Figure(
        data=go.Scatter(
            y=state.door_open_height, 
            x=state.timestamp, 
            mode='lines', 
            line_shape='hv'
        )
    ).update_layout(
        title="Door Open Height vs Time", 
        yaxis_title="Door Open Height (%)"
    )


# Local on_action
def execute(state, id):
    set_mode(state.mode_value)
    page_refresh(state)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Identity: Taipy | Mode Set To: {state.mode_value} |")
    
    if state.mode_value == "MANUAL":
        if float(state.table_data.get('Door Height(%)')[0]) > float(state.door_height):
            state.action_type = "CLOSE"
        elif float(state.table_data.get('Door Height(%)')[0]) < float(state.door_height):
            state.action_type = "OPEN"
        else:
            state.action_type = "NONE"
            
        data = {"water_level": "-", "water_pressure": "-", "fo_height": "-", "fo_width": "-", "inflow_velocity": "-", "emergency_status": "-", "action_type": state.action_type, "door_open_height": state.door_height, "action_remark": "MANUAL", "timestamp": datetime.now().strftime("%d:%m:%Y %H:%M:%S")}
        print(f"[{timestamp}] Identity: Taipy | Door Height Set To: {state.door_height} |")
        
        update_manual_data(data)    
        page_refresh(state)
    else:
        page_refresh(state)
    
    
pages = {
    "/" : page_0,
    "CHART" : page_1,
    "TABLE" : page_2,
    "CONTROL" : page_3
}    

# Load env vars
load_dotenv()        
Gui(pages=pages).run(use_reloader=True, debug=False, port=3000)
