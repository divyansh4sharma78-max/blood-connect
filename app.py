import os
from flask import Flask, render_template, request, jsonify
import urllib.request
import json

app = Flask(__name__)

# Mock data for blood banks and donors (fallback / initial state)
blood_banks = [
    {"id": 1, "name": "Red Cross Blood Bank", "city": "Bhopal", "address": "Near TT Nagar Stadium, Bhopal", "lat": 23.2353, "lng": 77.4019, "phone": "+91 755-2551234", "stock": {"A+": 14, "A-": 3, "B+": 22, "B-": 4, "AB+": 8, "AB-": 2, "O+": 30, "O-": 5}},
    {"id": 2, "name": "Hamidia Hospital Blood Center", "city": "Bhopal", "address": "Sultania Rd, Bhopal", "lat": 23.2531, "lng": 77.3976, "phone": "+91 755-2740123", "stock": {"A+": 8, "A-": 1, "B+": 12, "B-": 2, "AB+": 5, "AB-": 1, "O+": 19, "O-": 3}},
    {"id": 3, "name": "Chirayu Medical Blood Bank", "city": "Bhopal", "address": "Bairagarh, Indore Road, Bhopal", "lat": 23.2945, "lng": 77.3298, "phone": "+91 755-6603000", "stock": {"A+": 25, "A-": 6, "B+": 31, "B-": 7, "AB+": 14, "AB-": 4, "O+": 42, "O-": 8}},
    {"id": 4, "name": "Choithram Hospital Blood Bank", "city": "Indore", "address": "Manik Bagh Road, Indore", "lat": 22.7012, "lng": 75.8577, "phone": "+91 731-2402121", "stock": {"A+": 30, "A-": 7, "B+": 28, "B-": 5, "AB+": 12, "AB-": 3, "O+": 50, "O-": 10}}
]

donors_list = [
    {"id": 1, "name": "Amit Verma", "group": "O+", "city": "Bhopal", "phone": "+91 9826012345", "lastDonation": "3 months ago"},
    {"id": 2, "name": "Priya Singh", "group": "A+", "city": "Bhopal", "phone": "+91 9425054321", "lastDonation": "4 months ago"}
]

@app.route('/')
def index():
    return render_template('index.html', banks=blood_banks, donors=donors_list)

@app.route('/api/gemini-consult', methods=['POST'])
def gemini_consult():
    data = request.get_json() or {}
    user_prompt = data.get('prompt', '')
    
    api_key = os.environ.get("GEMINI_API_KEY", "")
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"You are an expert emergency medical and blood donation coordinator assistant. Provide a helpful, accurate, and concise response to this query: {user_prompt}"}]
        }],
        "systemInstruction": {
            "parts": [{"text": "You are a professional medical assistant specialized in blood banking and emergency health triage."}]
        }
    }
    
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(api_url, data=req_data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            candidate = res_json.get('candidates', [{}])[0]
            text_out = candidate.get('content', {}).get('parts', [{}])[0].get('text', 'Unable to retrieve AI analysis.')
            return jsonify({"result": text_out})
    except Exception as e:
        return jsonify({"result": f"Error communicating with Gemini model: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
