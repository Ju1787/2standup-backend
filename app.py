

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue sur votre API backend pour les soirées de stand-up!"

# Mock database structures
users = []
slots = []
reservations = []

# Endpoint: Register User
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    user_id = len(users) + 1
    data['id'] = user_id
    users.append(data)
    return jsonify({"message": "User registered successfully!", "user": data}), 201

# Endpoint: Create Slot
@app.route('/slots', methods=['POST'])
def create_slot():
    data = request.json
    slot_id = len(slots) + 1
    data['id'] = slot_id
    slots.append(data)
    return jsonify({"message": "Slot created successfully!", "slot": data}), 201

# Endpoint: View All Slots
@app.route('/slots', methods=['GET'])
def view_slots():
    return jsonify({"slots": slots}), 200

@app.route('/reservations', methods=['POST'])
def make_reservation():
    data = request.json
    if 'user_id' not in data or 'slot_id' not in data:
        return jsonify({"error": "Missing user_id or slot_id"}), 400
    reservation_id = len(reservations) + 1
    data['id'] = reservation_id
    reservations.append(data)
    return jsonify({
        "message": "Reservation created successfully!",
        "reservation": data
    }), 201

@app.route('/reservations', methods=['GET'])
def get_reservations():
    return jsonify({"reservations": reservations}), 200
