import logging
import os

from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/alexa")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


