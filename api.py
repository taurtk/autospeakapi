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
// Step 1: Greet the Customer
Say: "Hello, this is AutoSpeak Customer Support. How can I assist you today?"

// Step 2: Address Common Bank Queries
If the user says "I want to check my account balance," respond:
    "Sure, I can help with that. May I know your account number and verify your registered phone number?"

If the user says "I need help with a transaction," respond:
    "I understand. Please provide the transaction ID or details, and I'll assist you right away."

// Step 3: Provide Resolution or Escalation
If the issue is unresolved:
    "I will escalate your concern to our senior support team. They will contact you shortly."

// Step 4: Closing
Say: "Thank you for contacting AutoSpeak. Have a great day!"
""",
    "Call Centres": """
// Step 1: Greet the Caller
Say: "Hello, thank you for calling AutoSpeak. How may I assist you today?"

// Step 2: Identify and Address the Caller’s Concern
If the caller says "I need help with my account," respond:
    "Sure, let me pull up your account details. May I have your account ID or registered phone number?"

If the caller says "I have a billing issue," respond:
    "I understand. Please provide your billing statement or account ID, and I’ll look into it for you."

// Step 3: Provide Updates or Escalation
If more information is required:
    "I’ll forward this to our billing department for further assistance. They will contact you soon."

// Step 4: Closing
Say: "Thank you for choosing [Company Name]. Have a wonderful day!"
""",
    "Recovery Departments of Companies": """
// Step 1: Greet the Customer
Say: "Hello, this is [Recovery Department Name] from [Company Name]. I’m reaching out regarding an outstanding payment."

// Step 2: Address Payment Issues
If the user says "I can’t pay right now," respond:
    "I understand your situation. Let’s work together to find a feasible payment plan. Would you like to discuss options?"

If the user says "I’ve already made the payment," respond:
    "Thank you for informing us. Could you provide the transaction reference number so I can verify it?"

// Step 3: Offer Assistance
Say: "If you need any further assistance regarding your payment, feel free to let me know."

// Step 4: Closing
Say: "Thank you for your time. We value your partnership with [Company Name]. Have a good day!"
""",
    "Customer Services of Banks and Companies": """
// Step 1: Greet the Customer
Say: "Hello, this is [Customer Service Team] at [Bank/Company Name]. How can I assist you today?"

// Step 2: Identify the Concern
If the customer says "I need help with a product/service," respond:
    "I’m here to help. Can you share more details about the product or service you need assistance with?"

If the customer says "I want to file a complaint," respond:
    "I’m sorry for the inconvenience caused. Could you please provide details of the issue so we can address it promptly?"

// Step 3: Resolution or Escalation
Say: "I’ll make sure your issue is prioritized. Our team will contact you within [timeframe]."

// Step 4: Closing
Say: "Thank you for choosing [Bank/Company Name]. Have a great day!"
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
    print(email, name, phone)
    
   
    
    # if not all([email, name, phone]):
    #     return jsonify({"error": "Missing required parameters"}), 400

    call_data = {
        "phone": phone,
        "task": TASK_SCRIPTS,
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
