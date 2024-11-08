from taipy import Gui
from datetime import datetime
import plotly.graph_objects as go
from config.firebase_firestore_config import fetch_data, set_mode, update_manual_data


mode_value = "AUTO"
action_type = "OPEN"
door_height = 0
show_ele = False 

data = fetch_data()
door_open_height = data.get('Door Height(%)')
timestamp = data.get('Date Time')
fig = go.Figure(data=go.Scatter(y=door_open_height, x=timestamp)).update_layout(title="Door Open Height vs Time", yaxis_title="Door Open Height (%)")

page = """
# Data Representation <|Refresh|button|on_action=on_refresh|>

<|chart|figure={fig}|>
<br />
<br />

## Mode Selection
<|layout|columns=1 1 1 1|
<|{mode_value}|selector|lov=MANUAL;AUTO;|dropdown|label=Mode|on_change=mode_toggle|>

<|part|render={show_ele}
<|{action_type}|selector|lov=OPEN;CLOSE;|dropdown|label=Action Type|>
|>

<|part|render={show_ele}
<|{door_height}|selector|lov=0;10;20;30;40;50;60;70;80;90;100;|dropdown|label=Door Height(%)|>
|>

<|part|render={show_ele}
<|execute|button|on_action=on_execute|id=exe-btn|>
|>
|>

<br />
<br />
## Data Table
<|{data}|table|>
"""
def mode_toggle(state):
    if state.mode_value == "MANUAL":
        state.show_ele = True
    else:
        state.show_ele = False
        set_mode(state.mode_value)
        on_refresh(state)
        
def on_refresh(state):
    new_data = fetch_data()
    state.data = new_data
    state.door_open_height = new_data.get('Door Height(%)')
    state.timestamp = new_data.get('Date Time')
    state.fig = go.Figure(data=go.Scatter(y=state.door_open_height, x=state.timestamp)).update_layout(title="Door Open Height vs Time", yaxis_title="Door Open Height (%)")

def on_execute(state):
    if state.mode_value == "MANUAL":
        set_mode(state.mode_value)
        data = {"water_level": "-", "water_pressure": "-", "fo_height": "-", "fo_width": "-", "inflow_velocity": "-", "emergency_status": "-", "action_type": state.action_type, "door_open_height": state.door_height, "action_remark": "MANUAL", "timestamp": datetime.now().strftime("%d:%m:%Y %H:%M:%S")}
        update_manual_data(data)
        
    on_refresh(state)
        
Gui(page).run(use_reloader=True, debug=False, port=3000)
