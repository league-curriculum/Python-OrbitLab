#!/bin/bash

# Update pip to the latest version
python3 -m pip install --upgrade pip

# Check if requirements.txt exists in the root of the workspace
if [ -f "requirements.txt" ]; then
    pip3 install --user -r requirements.txt
fi

