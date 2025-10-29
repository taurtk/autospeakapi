from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API Key
BLAND_API_KEY = 'API_KEY'

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
 Step 4: Non Bank related queries
 If the user says: "non bank related queries like who is the president of united states," response:
 "Sure I can help with that. *2020:*
- *Global:* COVID-19 pandemic spreads worldwide, leading to lockdowns and economic downturns.
- *United States:* Joe Biden wins presidential election, defeating Donald Trump.
- *United Kingdom:* Brexit officially finalized on January 31.
- *Australia:* Massive bushfires destroy millions of acres of land.

*2021:*
- *Myanmar:* Military coup overthrows Aung San Suu Kyi's government.
- *Afghanistan:* U.S. withdrawal leads to the Taliban regaining control.
- *Japan:* Tokyo Summer Olympics held after a one-year delay.
- *Global:* COVID-19 vaccination campaigns accelerate worldwide.

*2022:*
- *Ukraine:* Russia invades Ukraine, triggering a major war and global sanctions on Russia.
- *United Kingdom:* Queen Elizabeth II passes away; King Charles III takes the throne.
- *France:* Emmanuel Macron re-elected as President.
- *Global:* The Omicron variant drives new COVID-19 waves.

*2023:*
- *Brazil:* Luiz Inácio Lula da Silva returns as President.
- *Turkey & Syria:* Devastating earthquake causes thousands of casualties.
- *Global:* AI adoption increases with tools like ChatGPT gaining popularity.
- *Sudan:* Military conflict erupts between rival factions.

*2024:*
- *United States:* Donald Trump wins the presidential election.
- *Israel & Gaza:* Escalation in the conflict leads to international intervention.
- *India:* Becomes the world’s most populous country, surpassing China.
- *Global:* Climate change initiatives gain momentum with stricter carbon reduction commitments.

*2025 (Jan-Feb):*
- *Global:* WHO announces plans for a pandemic treaty by mid-2025.
- *Russia:* Analysts predict internal challenges for President Vladimir Putin.
- *Global:* Economic slowdown due to geopolitical tensions and COVID-19 aftermath.

*Countries and Capital Cities Information:*

- *Afghanistan:* Kabul
- *Albania:* Tirana
- *Algeria:* Algiers
- *Andorra:* Andorra la Vella
- *Angola:* Luanda
- *Argentina:* Buenos Aires
- *Armenia:* Yerevan
- *Australia:* Canberra
- *Austria:* Vienna
- *Azerbaijan:* Baku
- *Bahamas:* Nassau
- *Bahrain:* Manama
- *Bangladesh:* Dhaka
- *Barbados:* Bridgetown
- *Belarus:* Minsk
- *Belgium:* Brussels
- *Belize:* Belmopan
- *Benin:* Porto-Novo
- *Bhutan:* Thimphu
- *Bolivia:* Sucre (constitutional), La Paz (seat of government)
- *Bosnia and Herzegovina:* Sarajevo
- *Botswana:* Gaborone
- *Brazil:* Brasília
- *Brunei:* Bandar Seri Begawan
- *Bulgaria:* Sofia
- *Burkina Faso:* Ouagadougou
- *Burundi:* Gitega
- *Cambodia:* Phnom Penh
- *Cameroon:* Yaoundé
- *Canada:* Ottawa
- *Central African Republic:* Bangui
- *Chad:* N'Djamena
- *Chile:* Santiago
- *China:* Beijing
- *Colombia:* Bogotá
- *Comoros:* Moroni
- *Congo, Democratic Republic of the:* Kinshasa
- *Congo, Republic of the:* Brazzaville
- *Costa Rica:* San José
- *Croatia:* Zagreb
- *Cuba:* Havana
- *Cyprus:* Nicosia
- *Czech Republic:* Prague
- *Denmark:* Copenhagen
- *Djibouti:* Djibouti
- *Dominica:* Roseau
- *Dominican Republic:* Santo Domingo
- *Ecuador:* Quito
- *Egypt:* Cairo
- *El Salvador:* San Salvador
- *Equatorial Guinea:* Malabo
- *Eritrea:* Asmara
- *Estonia:* Tallinn
- *Eswatini:* Mbabane (administrative), Lobamba (legislative, royal)
- *Ethiopia:* Addis Ababa
- *Fiji:* Suva
- *Finland:* Helsinki
- *France:* Paris
- *Gabon:* Libreville
- *Gambia:* Banjul
- *Georgia:* Tbilisi
- *Germany:* Berlin
- *Ghana:* Accra
- *Greece:* Athens
- *Guatemala:* Guatemala City
- *Guinea:* Conakry
- *Haiti:* Port-au-Prince
- *Honduras:* Tegucigalpa
- *Hungary:* Budapest
- *Iceland:* Reykjavik
- *India:* New Delhi
- *Indonesia:* Jakarta
- *Iran:* Tehran
- *Iraq:* Baghdad
- *Ireland:* Dublin
- *Israel:* Jerusalem
- *Italy:* Rome
- *Jamaica:* Kingston
- *Japan:* Tokyo
- *Jordan:* Amman
- *Kazakhstan:* Nur-Sultan
- *Kenya:* Nairobi
- *Kuwait:* Kuwait City
- *Kyrgyzstan:* Bishkek
- *Laos:* Vientiane
- *Latvia:* Riga
- *Lebanon:* Beirut
- *Liberia:* Monrovia
- *Libya:* Tripoli
- *Liechtenstein:* Vaduz
- *Lithuania:* Vilnius
- *Luxembourg:* Luxembourg City

*Southeast Asian Countries: A Comprehensive Overview*

Southeast Asia is a region in Asia consisting of 11 countries. It is known for its diverse cultures, rich history, and significant economic growth. Below is a detailed overview of each Southeast Asian country.

---

## *1. Brunei Darussalam*
- *Capital:* Bandar Seri Begawan  
- *Official Language:* Malay  
- *Currency:* Brunei Dollar (BND)  
- *Government:* Absolute Monarchy  
- *Economy:* Heavily reliant on oil and gas exports, Brunei enjoys one of the highest per capita incomes in the world.  
- *Culture & Tourism:* Known for its Islamic heritage, Brunei features landmarks like the Omar Ali Saifuddien Mosque and Ulu Temburong National Park.

---

## *2. Cambodia*
- *Capital:* Phnom Penh  
- *Official Language:* Khmer  
- *Currency:* Cambodian Riel (KHR)  
- *Government:* Constitutional Monarchy  
- *Economy:* Agriculture, garment industry, and tourism are key contributors.  
- *Culture & Tourism:* Home to the Angkor Wat temple complex, Cambodia has a rich cultural and historical heritage.

---

## *3. Indonesia*
- *Capital:* Jakarta  
- *Official Language:* Indonesian  
- *Currency:* Indonesian Rupiah (IDR)  
- *Government:* Presidential Republic  
- *Economy:* Largest economy in Southeast Asia, major industries include manufacturing, tourism, and palm oil production.  
- *Culture & Tourism:* Famous for Bali, Borobudur Temple, and diverse ethnic traditions across 17,000+ islands.

---

## *4. Laos*
- *Capital:* Vientiane  
- *Official Language:* Lao  
- *Currency:* Lao Kip (LAK)  
- *Government:* Socialist Republic  
- *Economy:* Hydropower, agriculture, and tourism are key industries.  
- *Culture & Tourism:* Known for Luang Prabang, a UNESCO World Heritage site, and its Buddhist traditions.

---

## *5. Malaysia*
- *Capital:* Kuala Lumpur  
- *Official Language:* Malay  
- *Currency:* Malaysian Ringgit (MYR)  
- *Government:* Federal Constitutional Monarchy  
- *Economy:* Major industries include manufacturing, palm oil, and electronics.  
- *Culture & Tourism:* Famous for the Petronas Towers, diverse cuisine, and tropical islands.

---

## *6. Myanmar*
- *Capital:* Naypyidaw  
- *Official Language:* Burmese  
- *Currency:* Myanmar Kyat (MMK)  
- *Government:* Military Junta  
- *Economy:* Agriculture, mining, and textiles are key sectors.  
- *Culture & Tourism:* Home to Bagan’s ancient temples and the golden Shwedagon Pagoda.

---

## *7. Philippines*
- *Capital:* Manila  
- *Official Language:* Filipino, English  
- *Currency:* Philippine Peso (PHP)  
- *Government:* Presidential Republic  
- *Economy:* Major industries include BPO services, agriculture, and remittances.  
- *Culture & Tourism:* Known for its beaches like Boracay and Palawan, as well as Spanish colonial history.

---

## *8. Singapore*
- *Capital:* Singapore  
- *Official Languages:* English, Malay, Tamil, Mandarin  
- *Currency:* Singapore Dollar (SGD)  
- *Government:* Parliamentary Republic  
- *Economy:* A global financial hub with strong sectors in technology, logistics, and trade.  
- *Culture & Tourism:* Marina Bay Sands, Sentosa Island, and its multicultural heritage.

---

## *9. Thailand*
- *Capital:* Bangkok  
- *Official Language:* Thai  
- *Currency:* Thai Baht (THB)  
- *Government:* Constitutional Monarchy  
- *Economy:* Tourism, manufacturing, and agriculture are key industries.  
- *Culture & Tourism:* Known for Thai cuisine, Buddhist temples, and vibrant nightlife.

---

## *10. Timor-Leste*
- *Capital:* Dili  
- *Official Languages:* Tetum, Portuguese  
- *Currency:* US Dollar (USD)  
- *Government:* Semi-Presidential Republic  
- *Economy:* Relies on oil revenues, agriculture, and coffee exports.  
- *Culture & Tourism:* Colonial architecture and pristine beaches attract visitors.

---

## *11. Vietnam*
- *Capital:* Hanoi  
- *Official Language:* Vietnamese  
- *Currency:* Vietnamese Dong (VND)  
- *Government:* Socialist Republic  
- *Economy:* Rapidly growing, with major industries in textiles, electronics, and tourism.  
- *Culture & Tourism:* Halong Bay, Ho Chi Minh City, and historical sites from the Vietnam War era.

---

## *Regional Overview*

### *Geography*
Southeast Asia is geographically divided into:
- *Mainland Southeast Asia (Indochina)*: Myanmar, Thailand, Laos, Cambodia, Vietnam.
- *Maritime Southeast Asia*: Indonesia, Malaysia, Philippines, Singapore, Brunei, Timor-Leste.

### *Economy*
The region is a key player in global trade, driven by manufacturing, agriculture, and tourism. ASEAN (Association of Southeast Asian Nations) plays a vital role in economic integration.

### *Culture*
A melting pot of cultures influenced by Indian, Chinese, and Islamic traditions. Major religions include Buddhism, Islam, and Christianity.

### *Tourism*
Tourism is a major contributor to GDP, with famous attractions like Bali, Angkor Wat, and Halong Bay.

### *Challenges & Opportunities*
- *Challenges:* Political instability, environmental concerns, and income inequality.
- *Opportunities:* Emerging markets, technological advancements, and growing digital economies."

// Step 5: Closing
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
# Function to poll call details
def poll_call_details(call_id):
    url = "https://api.bland.ai/logs"
    data = {"call_id": call_id}
    headers = {"Authorization": f"Bearer {BLAND_API_KEY}", "Content-Type": "application/json"}

    retries = 10
    delay = 15  # Seconds between retries

    for attempt in range(retries):
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                call_details = response.json()
                if call_details.get('queue_status', '').lower() in ['complete', 'completed']:
                    return call_details
            time.sleep(delay)
        except Exception as e:
            return {"error": str(e)}

    return {"error": "Call did not complete within the allowed attempts"}

@app.route('/initiate-call', methods=['POST'])
def initiate_call():
    try:
        # Determine if the request is JSON or form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form  # Handle form-encoded data

        # Extract and validate required fields
        email = data.get("email")
        name = data.get("name")
        phone = data.get("phone")

        if not all([email, name, phone]):
            return jsonify({"error": "Missing required parameters: 'email', 'name', and 'phone' are mandatory"}), 400

        # Prepare call data
        call_data = {
            "phone_number": phone,
            "task": TASK_SCRIPTS.get("Banks", "Default Task"),  # Adjust task category as needed
            "summarize": True,
            "record": True,
             "webhook": "https://webhook-6owf.onrender.com/grok-webhook"
        }

        headers = {"Authorization": f"Bearer {BLAND_API_KEY}", "Content-Type": "application/json"}

        # Send the API request to initiate the call
        response = requests.post(
            "https://api.bland.ai/call",
            json=call_data,
            headers=headers
        )

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

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request error: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
