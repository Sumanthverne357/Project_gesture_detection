#!/bin/bash

# Set the path to your virtual environment's activate script
VENV_PATH="Project_gesture_detection/ble_env/bin"

# Check if the activate script exists
if [ -f "$VENV_PATH" ]; then
    # Activate the virtual environment
    source "$VENV_PATH"
    
    # Define a function to handle Ctrl+C
    ctrl_c() {
        echo "Ctrl+C detected. Deactivating virtual environment and exiting."
        deactivate
        exit 1
    }

    # Trap Ctrl+C to call the function
    trap ctrl_c INT
    
    # Loop indefinitely until interrupted by Ctrl+C
    while true; do
        python /home/sharath/gesture_project/Project_gesture_detection/app.py
        sleep 1
    done
else
    echo "Virtual environment not found at $VENV_PATH"

    exit 1
fi