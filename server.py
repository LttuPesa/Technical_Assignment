from flask import Flask, request, jsonify

app = Flask(__name__)

TEMP_DATA = []
HUM_DATA = []

@app.route("/")
def root_route():
    return "Hallo Mamank"

@app.route("/temp", methods=["GET"])
def get_temp():
    return jsonify(TEMP_DATA)

@app.route("/hum", methods=["GET"])
def get_hum():
    return jsonify(HUM_DATA)

@app.route("/submit-temp", methods=["POST"])
def post_temp():
    pesan = request.data.decode("utf8")
    try:
        temperature = float(pesan)
        TEMP_DATA.append(temperature)
        print(f"Received temperature: {temperature}")
        return jsonify({"message": "Received temperature", "temperature": temperature}), 200
    except ValueError:
        return jsonify({"error": "Invalid temperature data"}), 400

@app.route("/submit-hum", methods=["POST"])
def post_hum():
    pesan = request.data.decode("utf8")
    try:
        humidity = float(pesan)
        HUM_DATA.append(humidity)
        print(f"Received humidity: {humidity}")
        return jsonify({"message": "Received humidity", "humidity": humidity}), 200
    except ValueError:
        return jsonify({"error": "Invalid humidity data"}), 400

@app.route("/submit", methods=["POST"])
def post_data():
    pesan = request.get_json()
    if "temp" in pesan and "hum" in pesan:
        try:
            temperature = float(pesan["temp"])
            humidity = float(pesan["hum"])
            TEMP_DATA.append(temperature)
            HUM_DATA.append(humidity)
            print(f"Received data: {pesan}")
            return jsonify({"message": "Received data", "temperature": temperature, "humidity": humidity}), 200
        except ValueError:
            return jsonify({"error": "Invalid data format"}), 400
    else:
        return jsonify({"error": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
