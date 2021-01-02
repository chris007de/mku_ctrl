#!/usr/bin/python3

# MIT License
#
# Copyright (c) 2021 Christian Obersteiner, DL1COM
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import argparse
from flask import Flask, request, jsonify, render_template
import jsend
from mku_up_2424_b import MKU_UP_2424_B, ConverterError

def create_app():
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'static')
        app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    else:
        app = Flask(__name__)

    app.config["DEBUG"] = True
    converter = MKU_UP_2424_B()
    return app, converter

app, converter = create_app()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/get/<string:status>', methods=['GET'])
def handle_get(status: str):
    try:
        response, text = converter.read_status(status)
        message = jsend.success(
            {"response":response, "response_text":text})
    except ConverterError as e:
        message = jsend.error(e.message)

    return jsonify(message)

@app.route('/set/converter_state/<int:state>', methods=['GET','POST'])
def handle_set_converter_state(state: str):
    try:
        message = jsend.success({"converter_state":converter.set_converter_state(state)})
    except ConverterError as e:
        message = jsend.error(e.message)

    return jsonify(message)

if __name__ == '__main__':
    print("Starting App")
    description = "Kuhne MKU 2424 B Remote Control by DL1COM v1.0"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("port", help="Upconverter Serial Port", nargs=1)
    args = parser.parse_args()
    converter.set_serial_port(args.port[0])
    app.run(host= '0.0.0.0')
