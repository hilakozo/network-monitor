#!/bin/bash

#!/bin/bash

# Function to setup script to run at boot
setup_cron_job() {
    # Capture low and high threshold parameters
    local LOW_THRESHOLD=$1
    local HIGH_THRESHOLD=$2
    local SCRIPT_DIR=$(dirname "$0")
    local VENV_PATH="$SCRIPT_DIR/venv/bin/python"
    local SCRIPT_PATH="$SCRIPT_DIR/main.py"

    (crontab -l 2>/dev/null; echo "@reboot $VENV_PATH $SCRIPT_PATH --low $LOW_THRESHOLD --high $HIGH_THRESHOLD") | crontab -

    # Optional: Confirm the crontab entry
    echo "Crontab entry added:"
    crontab -l
}

# Collect user input for thresholds
echo "Enter the low threshold for network packet rate (default 2):"
read low_threshold
if [ -z "$low_threshold" ]; then
    low_threshold=2
fi

echo "Enter the high threshold for network packet rate (default 50):"
read high_threshold
if [ -z "$high_threshold" ]; then
    high_threshold=50
fi

echo "Do you want to display the network graph? (yes/no)"
read graph_response
graph=""
if [[ "$graph_response" == "yes" ]]; then
    graph="--graph"
fi

# Call the function to setup cron job with user-specified thresholds
echo "Do you want to run alerts at start time? (yes/no)"
read cron_response
if [[ "$cron_response" == "yes" ]]; then
  setup_cron_job $low_threshold $high_threshold
fi


#echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Determine if the graph should be displayed

# Run the Python script with the user-specified options
echo "Starting the application..."
python main.py --low $low_threshold --high $high_threshold $graph
