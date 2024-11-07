@echo off
echo Running all scripts concurrently

REM
start python -m subscriber.subscriber_all
start python -m subscriber.subscriber_command