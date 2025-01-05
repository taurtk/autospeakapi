from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API Key
BLAND_API_KEY = 'org_8eabc93849311b46844d2ff69b684f544bf7adb1ed6a4b93b328e92791bfa79e1909301b43eadc679bde69'

# Task Scripts
TASK_SCRIPTS = {
    "Banks": """
    // Task script for Banks
    """,
    "Call Centres": """
    // Task script for Call Centres
    """,
    "Recovery Departments of Companies": """
    // Task script for Recovery Departments
    """,
    "Customer Services of Banks and Companies": """
    // Task script for Customer Services
    """
}

# Endpoint to fetch task scripts based on category
@app.route('/get-task-script', methods=['GET'])
def get_task_script():
    category = request.args.get('category')
    if category in TASK_SCRIPTS:
        return jsonify({"task_script": TASK_SCRIPTS[category]})
    else:
        return jsonify({"error": "Invalid category"}), 400

# Function to poll call details
def poll_call_details(call_id):
    url = "https://api.bland.ai/logs"
    data = {"call_id": call_id}
    headers = {"Authorization": f"Bearer {BLAND_API_KEY}", "Content-Type": "application/json"}
    
    retries = 10
    delay = 15  # Seconds between retries

    for attempt in range(retries):
        try:
            response = requests.post(url, json=data, headers=headers, proxies={"http": None, "https": None})
            if response.status_code == 200:
                call_details = response.json()
                if call_details.get('queue_status', '').lower() in ['complete', 'completed']:
                    return call_details
            time.sleep(delay)
        except Exception as e:
            return {"error": str(e)}

    return {"error": "Call did not complete within the allowed attempts"}

# Endpoint to initiate an outbound call
@app.route('/initiate-call', methods=['POST'])
def initiate_call():
    data = request.json
    print(data)
    email = data.get("email")
    name = data.get("name")
    phone = data.get("phone")
    
   
    
    if not all([email, name, phone]):
        return jsonify({"error": "Missing required parameters"}), 400

    call_data = {
        "phone": phone,
        "task": "Your default task script here",
        "summarize": True,
        "record": True
    }

    headers = {"Authorization": f"Bearer {BLAND_API_KEY}", "Content-Type": "application/json"}
    try:
        response = requests.post("https://api.bland.ai/call", json=call_data, headers=headers, proxies={"http": None, "https": None})
        if response.status_code == 200:
            call_response = response.json()
            call_id = call_response.get("call_id")
            if call_id:
                call_details = poll_call_details(call_id)
                return jsonify({
                    "call_response": call_response,
                    "call_details": call_details
                })
            else:
                return jsonify({"error": "Call ID not found in response"}), 500
        else:
            return jsonify({"error": response.text}), response.status_code
    except requests.exceptions.ProxyError as e:
        return jsonify({"error": f"Proxy error: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
