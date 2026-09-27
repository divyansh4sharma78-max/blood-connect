import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

blood_banks_data = [
    { "id": 1, "name": "Red Cross Blood Bank", "city": "Bhopal", "address": "Near TT Nagar Stadium, Bhopal", "lat": 23.2353, "lng": 77.4019, "phone": "+91 755-2551234", "stock": { "A+": 14, "A-": 3, "B+": 22, "B-": 4, "AB+": 8, "AB-": 2, "O+": 30, "O-": 5 } },
    { "id": 2, "name": "Hamidia Hospital Blood Center", "city": "Bhopal", "address": "Sultania Rd, Bhopal", "lat": 23.2531, "lng": 77.3976, "phone": "+91 755-2740123", "stock": { "A+": 8, "A-": 1, "B+": 12, "B-": 2, "AB+": 5, "AB-": 1, "O+": 19, "O-": 3 } },
    { "id": 3, "name": "Chirayu Medical Blood Bank", "city": "Bhopal", "address": "Bairagarh, Indore Road, Bhopal", "lat": 23.2945, "lng": 77.3298, "phone": "+91 755-6603000", "stock": { "A+": 25, "A-": 6, "B+": 31, "B-": 7, "AB+": 14, "AB-": 4, "O+": 42, "O-": 8 } },
    { "id": 4, "name": "Bansal Hospital Blood Bank", "city": "Bhopal", "address": "Shahpura, Bhopal", "lat": 23.2100, "lng": 77.4320, "phone": "+91 755-4086000", "stock": { "A+": 18, "A-": 4, "B+": 15, "B-": 3, "AB+": 9, "AB-": 2, "O+": 27, "O-": 6 } },
    { "id": 5, "name": "Choithram Hospital Blood Bank", "city": "Indore", "address": "Manik Bagh Road, Indore", "lat": 22.7012, "lng": 75.8577, "phone": "+91 731-2402121", "stock": { "A+": 30, "A-": 7, "B+": 28, "B-": 5, "AB+": 12, "AB-": 3, "O+": 50, "O-": 10 } },
    { "id": 6, "name": "MY Hospital Blood Bank", "city": "Indore", "address": "A.B. Road, Indore", "lat": 22.7196, lng: 75.8577, "phone": "+91 731-2527371", "stock": { "A+": 10, "A-": 2, "B+": 15, "B-": 1, "AB+": 4, "AB-": 0, "O+": 22, "O-": 4 } }
]

@app.route('/')
def index():
    return render_template('index.html', banks=blood_banks_data)

@app.route('/api/banks', methods=['GET'])
def get_banks():
    city = request.args.get('city', 'all')
    if city == 'all':
        return jsonify(blood_banks_data)
    filtered = [b for b in blood_banks_data if b['city'].lower() == city.lower()]
    return jsonify(filtered)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
