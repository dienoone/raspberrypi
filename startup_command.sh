#!/bin/bash

# Function to run meson devenv and execute the project
run_in_devenv() {
    meson devenv -C /home/pi/Downloads/libcamera/build <<EOF
    # Navigate to the project directory (if needed)
    cd /home/pi/Desktop/plant

    # Run your project (adjust the command as needed)
    python app.py

    echo "Project has been executed."
    exit
EOF
}

# Call the function
run_in_devenv
