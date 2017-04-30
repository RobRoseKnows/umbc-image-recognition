# Copyright 2017 Google Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Endpoints sample application.

Demonstrates how to create a simple API.
"""

import base64
import json
import logging
import io
import os
import urllib2, urllib
# Imports the Google Cloud client library
from google.cloud import vision

from flask import Flask, jsonify, request
from six.moves import http_client


app = Flask(__name__)


def _base64_decode(encoded_str):
    # Add paddings manually if necessary.
    num_missed_paddings = 4 - len(encoded_str) % 4
    if num_missed_paddings != 4:
        encoded_str += b'=' * num_missed_paddings
    return base64.b64decode(encoded_str).decode('utf-8')
def detect_text(path):
    """Detects text in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    texts = image.detect_text()
    text = texts[0].description
    print(text)

def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    uri_prefix = "https://s3.amazonaws.com/umbc-alexa-image-recognition/"
    uri = uri_prefix + uri
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)
    texts = image.detect_text()
    text = texts[0].description
    text = text.replace('\n', ' ').replace('\r',' ')
    return text

def get_description(uri):
    uri_prefix = "https://s3.amazonaws.com/umbc-alexa-image-recognition/"
    uri = uri_prefix + uri
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': os.environ["MS_SUB_KEY"],
    }
    body = {
        "url":uri,
        }
    try:
        endpoint_ms = "https://westus.api.cognitive.microsoft.com/vision/v1.0/describe?maxCandidates=1"
        request = urllib2.Request(endpoint_ms, data = json.dumps(body), headers = headers)
        response = urllib2.urlopen(request)
        
        toReturn =  response.read()
        toReturn = json.loads(toReturn)
        return toReturn["description"]["captions"][0]["text"]
    except Exception as e:
        print(e)
        

@app.route('/processmessage', methods=['POST'])
def process(event=None, context=None):
    """Process messages with information about S3 objects"""
    message = request.get_json().get('inputMessage', '')
    # add other processing as needed
    # for example, add event to PubSub topic or 
    # download object using presigned URL, save in Cloud Storage, invoke ML APIs
    text = detect_text_uri(message["Url"])
    return text

@app.route('/processimage', methods=['POST'])
def process_image(event=None, context=None):
    message = request.get_json().get('inputMessage', '')
    description = get_description(message["Url"])
    return description

@app.route('/')
def test(event=None, context=None):
    return "Testing 123"


@app.errorhandler(http_client.INTERNAL_SERVER_ERROR)
def unexpected_error(e):
    """Handle exceptions by returning swagger-compliant json."""
    logging.exception('An error occured while processing the request.')
    response = jsonify({
        'code': http_client.INTERNAL_SERVER_ERROR,
        'message': 'Exception: {}'.format(e)})
    response.status_code = http_client.INTERNAL_SERVER_ERROR
    return response


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(debug=True)
