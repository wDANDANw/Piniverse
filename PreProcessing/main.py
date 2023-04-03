# Main.py for Preprocessing Module

# Server
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

# Tokenization
from tokenization import EntityResolver

# NER
from ner import get_ner

# Entity parsing
from ner import parse_entities_standalone
from srl import fill_out_all_locations
from ner import convert_to_strings

# Gets a random quote
@app.route("/api/resolve_entity", methods=['POST'])
def resolve_entity():
    data = request.get_json()
    input_str = data["input_str"]
    resolver = EntityResolver([input_str])
    sequences = resolver.get_sequences()

    return jsonify({"raw": data, "sequences": sequences})

# Demo resolving for ner
@app.route("/api/resolve_ner", methods=['POST'])
def resolve_ner():
    data = request.get_json()
    input_str = data["input_str"]
    print(input_str)
    output = get_ner(input_str)

    print(output)

    return jsonify({"input": data, "output": output})

# Route to fully parse text into entities
@app.route("/api/parse_text_to_entities", methods=['POST'])
def parse_text_to_entities():
    print("parsing")  # TODO
    data = request.get_json()
    input_str = data["input_str"]

    # Entity processing
    print("Processing entity parsing request: ", input_str)
    output = parse_entities_standalone(input_str)
    print("Entities parsed: ", output)
    fill_out_all_locations(output)  # Modifies output in-place
    print("Entities located: ", output)
    convert_to_strings(output)  # Modifies output in-place

    return jsonify({"input": data, "output": output}) # TODO: Test if this works properly

# 404 Error for unknown routes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Resource not found"}), 404

#TODO: Temporary, for testing
'''
# 500 general-purpose error handler
@app.errorhandler(500)
def unknown_error(e):
    print("500 error encountered")
    return jsonify({"message": "Unknown internal error occurred"}), 500
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12334, debug=True) # run application #TODO: Changed port from 5000 to 12334 manually. may cause unexpected behavior
