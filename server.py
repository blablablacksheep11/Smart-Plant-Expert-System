
from flask import Flask, request, jsonify
from datetime import datetime
from services.supabase import supabase

app = Flask(__name__)

@app.route("/sensor-data", methods=["POST"])
def receive_sensor_data():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No sensor data received"}), 400

    try:
        response = (
            supabase.table("Environmental data")
            .insert(data)
            .execute()
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    return jsonify({
        "message": "Sensor data received successfully"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
