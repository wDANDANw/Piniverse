# Main.py for Preprocessing Module
import json
import os

# Server
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

# Environment
# https://danhwashere.com/flask-env-config
# https://flask.palletsprojects.com/en/2.2.x/config/#configuring-from-files
# https://stackoverflow.com/questions/15603240/flask-how-to-manage-different-environment-databases
app.config.from_object("default_settings")
app.config.from_envvar('CONFIG_PATH',silent=True)
print("Using Config: " + os.environ.get("CONFIG_PATH", default="default_settings"))

# Service Imports
from generator_apis import *

# Debug
GLOBAL_DEBUG_FLAG = app.config["DEBUG"]
DEBUG_INSTANCE = None
debug_file_path = "./debug.txt"
if os.path.exists(debug_file_path) and os.path.getsize(debug_file_path) > 0:
    with open(debug_file_path, "r", encoding="utf-8") as f:
        debug_store = json.loads(f.read())
        DEBUG_INSTANCE = debug_store["entities"], debug_store["scene"], debug_store["events"], debug_store["logics"]

# Analyze Story
@app.route("/api/analyze_story", methods=['POST'])
def analyze_story_api():

    # Function level debug flag
    debug = GLOBAL_DEBUG_FLAG

    if debug: print("Calling 'analyze_story'")

    data = request.get_json()
    query = data["query"]

    global DEBUG_INSTANCE
    if (debug):
        if (DEBUG_INSTANCE is None):
            entities, scene, events, logics = analyze_story(query)
            DEBUG_INSTANCE = entities, scene, events, logics
            with open(debug_file_path, "w", encoding="utf-8") as f:
                f.write(json.dumps({
                    "entities": entities,
                    "scene": scene,
                    "events": events,
                    "logics": logics
                }))
        else:
            entities, scene, events, logics = DEBUG_INSTANCE
    else:
        entities, scene, events, logics = analyze_story(query)

    if entities is None:
        return jsonify({"error": "Failed to generate"}), 500


    return jsonify({"entities": json.dumps(entities),
                    "scene": json.dumps(scene),
                    "events": json.dumps(events),
                    "logics": json.dumps(logics)})

# 404 Erorr for unknown routes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config["PORT"], debug=True) # run application
    