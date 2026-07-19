#!/usr/bin/env python3

import logging

from flask import Flask, jsonify, request
from keyboard_layout import read_layout
import keyboard_physical

app = Flask("Fakeys server")

#TODO: Should pre-load _all_ layouts

layout = read_layout("SW")

@app.route("/type_string/", methods=["POST"])
def typestring():

  if "string" not in request.json:
     return "no string specified!", 400 # 400: Bad Request

  string = request.json["string"]

  if not layout:
     return jsonify(["error", "No such layout"], 501) # 501: Not Implemented
  
  keyboard_physical.type(string, layout)

  # Error handling & return value evaluation
  errors = keyboard_physical.log_collector.get_records_dicts(logging.WARNING)
  if len(errors) > 0:
     return jsonify({"message": f"Failed to type {string}", "errors": errors}), 500
  
  return jsonify({"message": f"Successfully typed {string}"})

@app.route("/", methods=["GET"])
def home():
    #TODO: Static page that sends string to endpoint via POST
    return {"data": "Hello, World"}

if __name__ == '__main__':
    app.run(debug=True)