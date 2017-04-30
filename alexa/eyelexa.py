#!/bin/python3
import boto3
import logging
import os
import json
import urllib
import urllib2

from flask import Flask
from flask_ask import Ask, request, session, question, statement

# Doing this because there's also a "request" object in flask ask
import requests as _reqs

app = Flask(__name__)
ask = Ask(app, "/alexa")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    

    return


@ask.intent("DescribeIntent")
def describeIntent():

    
    return



@ask.intent("ReadIntent")
def readIntent():
    
    photoUrl = getPhoto()

    if(photoUrl == ""):
        return statement(
                "I encountered an error while checking for your image.")
    elif(photoUrl == "IMG_ERROR"):
        return statement(
                "I encountered an error while retrieving your image."
    elif(photoUrl == "AUTH_ERROR"):
        return statement(
                "I encountered an error while requesting your image.")
    else:
        googleReply = sendToGoogle(photoUrl)
        
    
        return ""

@ask.intent("SummarizeIntent")
def summarizeIntent():
    

def sendToGoogle(url):

    try:
        data = {"inputMessage": {
            "Url": url
            }
        }

        headers = {"Content-Type": "application/json",
            "x-api-key": os.environ["ENDPOINT_KEY"]
        }

        googleReply = _reqs.post(os.environ["ENDPOINT_URL"], 
            headers=headers, data=data)

        return googleReply
    except Exception as e:
        print(e)
        print('Error integrating lambda function with endpoint for url {}'
            .format(url)
        raise e


# Calls the laptop using ngrok and then 
# Returns: a URL to the photo in S3.
def getPhoto():
    try:
        photoUrl = _reqs.get(
                os.environ["NGROK_URL"], 
                { 'key': os.environ["NGROK_AUTH_KEY"] + })

    

