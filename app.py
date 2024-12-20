from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock databases
users = []
slots = []
reservations = []

# Helper functions for validation and retrieval
def find_user_by_id(user_id):
    """Find a user by ID."""
    return next((user for user in users if user['id'] == user_id), None)

def find_slot_by_id(slot_id):
    """Find a slot by ID."""
    return next((slot for slot in slots if slot['id'] == slot_id), None)

def is_slot_reserved(slot_id):
    """Check if a slot is already reserved."""
    return any(reservation['slot_id'] == slot_id for reservation in reservations)

# Routes
@app.route('/')
def home():
    return "Bienvenue sur votre API backend pour les soirées de stand-up!"

# Endpoint: Register User
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400

    if any(user['email'] == data['email'] for user in users):
        return jsonify({"error": "Email already registered"}), 400

    user_id = len(users) + 1
    new_user = {
        "id": user_id,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    return jsonify({"message": "User registered successfully!", "user": new_user}), 201

# Endpoint: Create Slot
@app.route('/slots', methods=['POST'])
def create_slot():
    data = request.json
    if 'date' not in data or 'time' not in data or 'location' not in data:
        return jsonify({"error": "Date, time, and location are required"}), 400

    slot_id = len(slots) + 1
    new_slot = {
        "id": slot_id,
        "date": data['date'],
        "time": data['time'],
        "location": data['location'],
        "type": data.get('type', 'General')
    }
    slots.append(new_slot)
    return jsonify({"message": "Slot created successfully!", "slot": new_slot}), 201

# Endpoint: View All Slots
@app.route('/slots', methods=['GET'])
def view_slots():
    return jsonify({"slots": slots}), 200

# Endpoint: Create Reservation
@app.route('/reservations', methods=['POST'])
def make_reservation():
    data = request.json
    if 'user_id' not in data or 'slot_id' not in data:
        return jsonify({"error": "User ID and Slot ID are required"}), 400

    user = find_user_by_id(data['user_id'])
    if not user:
        return jsonify({"error": "Invalid User ID"}), 400

    slot = find_slot_by_id(data['slot_id'])
    if not slot:
        return jsonify({"error": "Invalid Slot ID"}), 400

    if is_slot_reserved(data['slot_id']):
        return jsonify({"error": "Slot already reserved"}), 400

    reservation_id = len(reservations) + 1
    new_reservation = {
        "id": reservation_id,
        "user_id": data['user_id'],
        "slot_id": data['slot_id']
    }
    reservations.append(new_reservation)
    return jsonify({"message": "Reservation created successfully!", "reservation": new_reservation}), 201

# Endpoint: View All Reservations
@app.route('/reservations', methods=['GET'])
def get_reservations():
    return jsonify({"reservations": reservations}), 200

# Endpoint: Delete a Reservation
@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    global reservations
    reservation = next((r for r in reservations if r['id'] == reservation_id), None)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    reservations = [r for r in reservations if r['id'] != reservation_id]
    return jsonify({"message": "Reservation deleted successfully!"}), 200

# Endpoint: Update a Slot
@app.route('/slots/<int:slot_id>', methods=['PUT'])
def update_slot(slot_id):
    global slots
    data = request.json
    slot = find_slot_by_id(slot_id)
    if not slot:
        return jsonify({"error": "Slot not found"}), 404

    slot.update({
        "date": data.get('date', slot['date']),
        "time": data.get('time', slot['time']),
        "location": data.get('location', slot['location']),
        "type": data.get('type', slot['type'])
    })
    return jsonify({"message": "Slot updated successfully!", "slot": slot}), 200

if __name__ == '__main__':
    app.run(debug=True)
