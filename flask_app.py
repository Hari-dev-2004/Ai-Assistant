from flask import Flask, jsonify, render_template
import json
import time

app = Flask(__name__)

# Define the path to the conversation data file
json_file_path = "conversation_data.json"

def read_conversation():
    """Read the latest conversation data from the JSON file."""
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

@app.route('/get_conversation')
def get_conversation():
    """API endpoint to fetch the latest conversation data."""
    data = read_conversation()
    return jsonify(data)

@app.route('/')
def index():
    """Render the main interactive AI model page."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
