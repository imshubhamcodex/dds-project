from taipy import Gui
import plotly.graph_objects as go
from config.firebase_firestore_config import fetch_data

data = fetch_data()
door_open_height = data.get('By %')
timestamp = data.get('Date&Time(dd:mm:yyyyThh:mm:ss)')

fig = go.Figure(data=go.Scatter(y=door_open_height, x=timestamp))
fig.update_layout(title="Door Open Height vs Time", yaxis_title="Door Open Height (%)")

page = """
# Data Representaion   <|Refresh|button|>
<|chart|figure={fig}|>
# 
<|{data}|table|>
"""
def on_action(state, id):
    new_data = fetch_data() 
    state.data = new_data
    state.door_open_height = new_data.get('By %')
    state.timestamp = new_data.get('Date&Time(dd:mm:yyyyThh:mm:ss)')
    state.fig = go.Figure(data=go.Scatter(y=state.door_open_height, x=state.timestamp)).update_layout(title="Door Open Height vs Time", xaxis_title="Timestamp", yaxis_title="Door Open Height (%)")

    
Gui(page).run(use_reloader=True, debug=False, port=3000)