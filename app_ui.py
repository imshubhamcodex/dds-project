from taipy import Gui
from datetime import datetime
import plotly.graph_objects as go
from config.firebase_firestore_config import fetch_data, set_mode, update_manual_data


mode_value = "AUTO"
action_type = "OPEN"
door_height = 0
show_ele = True 


def get_table_data(data):
    data_key = data.keys()
    data_dict = {}
    for key in data_key:
        rev_val = data.get(key)
        data_dict[key] = rev_val[::-1]
    return data_dict
        
    
    
data = fetch_data()
table_data = get_table_data(data)

door_open_height = data.get('Door Height(%)')
timestamp = data.get('Date Time')
fig = go.Figure(data=go.Scatter(y=door_open_height, x=timestamp)).update_layout(title="Door Open Height vs Time", yaxis_title="Door Open Height (%)")

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
<|chart|figure={fig}|>
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
<|{mode_value}|selector|lov=MANUAL;AUTO;|dropdown|label=Mode|on_change=mode_toggle|>
|>
<|part|render={show_ele}
<|{door_height}|selector|lov=0;10;20;30;40;50;60;70;80;90;100;|dropdown|label=Door Height(%)|>
|>
<|part|render={show_ele}
<|execute|button|on_action=on_execute|id=exe-btn|>
|>
|>
#
|>
"""



def mode_toggle(state):
    print("Mode Changed To: ", state.mode_value)

    # if state.mode_value == "MANUAL":
    #     state.show_ele = True
    # else:
    #     state.show_ele = False
    #     on_refresh(state)
        
def on_refresh(state):
    new_data = fetch_data()
    state.data = new_data
    state.table_data = get_table_data(new_data)
    state.door_open_height = new_data.get('Door Height(%)')
    state.timestamp = new_data.get('Date Time')
    state.fig = go.Figure(data=go.Scatter(y=state.door_open_height, x=state.timestamp)).update_layout(title="Door Open Height vs Time", yaxis_title="Door Open Height (%)")

def on_execute(state):
    set_mode(state.mode_value)
    on_refresh(state)
    
    if state.mode_value == "MANUAL":
        if float(state.table_data.get('Door Height(%)')[0]) > float(state.door_height):
            state.action_type = "CLOSE"
        elif float(state.table_data.get('Door Height(%)')[0]) < float(state.door_height):
            state.action_type = "OPEN"
        else:
            state.action_type = "NONE"
            state.door_height = 0
            
        data = {"water_level": "-", "water_pressure": "-", "fo_height": "-", "fo_width": "-", "inflow_velocity": "-", "emergency_status": "-", "action_type": state.action_type, "door_open_height": state.door_height, "action_remark": "MANUAL", "timestamp": datetime.now().strftime("%d:%m:%Y %H:%M:%S")}
        update_manual_data(data)    
        on_refresh(state)
    else:
        on_refresh(state)
    
    
pages = {
    "CHART" : page_1,
    "TABLE" : page_2,
    "CONTROL" : page_3
}    
        
Gui(pages=pages).run(use_reloader=True, debug=False, port=3000)
