# Main.py for Preprocessing Module
import json
import os

# Server
from flask import Flask
from flask import jsonify
from flask import request, send_file

import io
import base64

app = Flask(__name__)

# Environment
app.config.from_object("default_settings")
app.config.from_envvar('CONFIG_PATH',silent=True)
print("Using Config: " + os.environ.get("CONFIG_PATH", default="default_settings"))

# Services
from candidates.openai_point_e.generator import text_to_pc

# Debug
GLOBAL_DEBUG_FLAG = app.config["DEBUG"]
DEBUG_PC_INSTANCE = None

# Route for getting text to model
@app.route("/api/text_to_model", methods=['POST'])
def text_to_3d_model():
    """
    The route of 3D Model Generator with Point E to return mesh based on text prompt
    Request: query: the string that contains the query. Should be only one entity.
    Response:
    Json object
        {
            query: string => For matching the name / metadata of the generated model
            geometry: obj
                {
                    coords: array
                    colors: array
                }
        }

    Note:
        It's better to just return the vertices & colors but not mesh because it's easier for
        data transmission and data loading at frontend
    """

    debug = GLOBAL_DEBUG_FLAG # Function level debug flag for testing frontend

    print("Calling 'text to 3d model'")

    # Process query
    data = request.get_json()
    query = data["query"]
    print("Query str: " + query)

    if debug:
        # If no pc instance, then create one. Else, use the previous and the only one (reduce generation time in debug)
        global DEBUG_PC_INSTANCE
        if DEBUG_PC_INSTANCE is None:
            DEBUG_PC_INSTANCE = text_to_pc(query)
        else:
            print("Returning first time queried pc")

        pc = DEBUG_PC_INSTANCE
    else:
        pc = text_to_pc(query)

    return jsonify({"query": query, "geometry": json.dumps(pc.to_serilizable())})

# 404 Erorr for unknown routes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Resource not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config["PORT"], debug=True)  # run application
