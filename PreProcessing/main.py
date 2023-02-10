# Main.py for Preprocessing Module

# Server
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

# Tokenization
from tokenization import EntityResolver

# Gets a random quote
@app.route("/api/resolve_entity", methods=['POST'])
def resolve_entity():
    data = request.get_json()
    input_str = data["input_str"]
    resolver = EntityResolver([input_str])
    sequences = resolver.get_sequences()

    return jsonify({"raw": data, "sequences": sequences})

# 404 Erorr for unknown routes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # run application
    