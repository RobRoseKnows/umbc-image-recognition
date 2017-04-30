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
#from constants import AskTasks 
import getters

app = Flask(__name__)
ask = Ask(app, "/alexa")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    card_title = render_template('card_title')
    return statement("This is the launch statement")

@ask.intent("AMAZON.CancelIntent")
def cancelIntent():
    return statement("This is the cancel intent")

@ask.intent("AMAZON.HelpIntent")
def helpIntent():
    return statement("This is the help intent")


@ask.intent("AMAZON.StopIntent")
def stopIntent():
    return statement("This is the stop intent")


@ask.intent("AMAZON.YesIntent")
def yesIntent():
    return statement("This is the yes intent")

@ask.intent("AMAZON.NoIntent")
def noIntent():
    return statement("This is the no intent")


@ask.intent("DescribeIntent")
def describeIntent():
    #session.attributes[constants.CURR_TASK] = AskTasks.desc_intent
    return


@ask.intent("ReadIntent")
def readIntent():
    #session.attributes[constants.CURR_TASK] = AskTasks.read_intent
    
    #return statement("This is the read intent")

    card_title = render_template('card_title')

    photoUrl = getters.getPhoto()

    if(photoUrl == ""):
        # This isn't as much of an error as it is a just a lack of text
        err_msg = render_template('err_no_txt')
        return statement(err_msg)
    # These two are general errors that might be triggered by different
    # things happening. They aren't very helpful, this is a hackathon.
    elif(photoUrl == "IMG_ERROR"):
        err_msg = render_template('err_img')
        return statement(err_msg)
    elif(photoUrl == "AUTH_ERROR"):
        err_msg = render_template('err_auth')
        return statement(err_msg)
    else:
        # Send our image to Google and get the text back
        googleReply = getters.getImageText(photoUrl)
        
        # If a lot of text is returned, we'll only take the first tweet and a
        # half. We send all of it to the Alexa app though.
        if(len(googleReply) > 210):
            message = render_template(
                    constants.GOOG_LARGE, text=googleReply[:210])
        else:
            message = render_template(
                    constants.GOOG_SMALL, text=googleReply)
        
        # Return the statement and send the thing to the card.
        return statement(message).simple_card(card_title, googleReply)
 
