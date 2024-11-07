@echo off
echo Running all scripts concurrently

REM
start python -m publisher.publisher_fo_width
start python -m publisher.publisher_fo_height
start python -m publisher.publisher_inflow_velocity
start python -m publisher.publisher_water_level
start python -m publisher.publisher_water_pressure
start python -m publisher.publisher_emergency_status