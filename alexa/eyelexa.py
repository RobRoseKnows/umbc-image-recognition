#!/bin/python3
import boto3
import logging
import os

# Flask stuff
from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement

# This is for the summarizer
import Algorithmia

# My very own files.
import constants
import getters

app = Flask(__name__)
ask = Ask(app, "/alexa")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    

    return

@ask.intent("AMAZON.CancelIntent")
def cancelIntent():

    return

@ask.intent("AMAZON.HelpIntent")
def helpIntent():

    return


@ask.intent("AMAZON.StopIntent")
def stopIntent():

    return


@ask.intent("AMAZON.YesIntent")
def yesIntent():

    return

@ask.intent("AMAZON.NoIntent")
def noIntent():

    return


@ask.intent("DescribeIntent")
def describeIntent():

    
    return


@ask.intent("ReadIntent")
def readIntent():
    
    photoUrl = getPhoto()

    if(photoUrl == ""):
        return statement(
                "I encountered an error while checking for your image. ")
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
    

