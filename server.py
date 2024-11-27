from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if not data or "heart_rate" not in data or "oxygen_level" not in data:
        return jsonify({"message": "Invalid data"}), 400

    print(f"Received data: {data}")
    return jsonify({"message": "Data received successfully"}), 200

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify({"heart_rate": 75, "oxygen_level": 98}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
