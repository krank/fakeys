#!/usr/bin/env python3

import logging

from flask import Flask, jsonify, request
from keyboard_layout import Layout, read_layout, get_available_layouts, default_layout
import keyboard_physical

app = Flask("Fakeys server")


@app.route("/type_string/", methods=["POST"])
def typestring():

    if "string" not in request.json:
        return "no string specified!", 400  # 400: Bad Request

    string = request.json["string"]

    if "layout" in request.json:
        layout_name = request.json["layout"].upper()
    else:
        layout_name = (
            default_layout if default_layout in layouts else list(layouts.keys())[0]
        )

    if layout_name not in layouts:
        return jsonify(
            ["error", f"No such layout: '{layout_name}'"], 501
        )  # 501: Not Implemented

    keyboard_physical.type(string, layouts[layout_name])

    # Error handling & return value evaluation
    errors = keyboard_physical.log_collector.get_records_dicts(logging.WARNING)
    if len(errors) > 0:
        return jsonify({"message": f"Failed to type {string}", "errors": errors}), 500

    return jsonify({"message": f"Successfully typed {string}"})


@app.route("/", methods=["GET"])
def home():
    # TODO: Static page that sends string to endpoint via POST
    return {"data": "Hello, World"}


layouts: dict[str, Layout] = {}

if __name__ == "__main__":

    # Prep keyboard layouts
    for layout_name in get_available_layouts():
        layout_maybe = read_layout(layout_name)
        if layout_maybe:
            layouts[layout_name] = layout_maybe

    # --------------------------------------------------------------------------
    app.run(debug=True)
