#echo "Setting up Python virtual environment..."
#python3 -m venv venv
#source venv/bin/activate
#echo "Installing dependencies from requirements.txt..."
#pip install -r requirements.txt

# Collect user input for thresholds
echo "Enter the low threshold for network packet rate (default 2):"
read low
if [ -z "$low" ]; then
    low=2
fi

echo "Enter the high threshold for network packet rate (default 50):"
read high
if [ -z "$high" ]; then
    high=50
fi
# Determine if the graph should be displayed
echo "Do you want to display the network graph? (yes/no)"
read graph_response
graph=""
if [[ "$graph_response" == "yes" ]]; then
    graph="--graph"
fi

# Run the Python script with the user-specified options
echo "Starting the application..."
python main.py --low $low --high $high $graph
