import io
import os

# Imports the Google Cloud client library
from google.cloud import vision

def detect_text(path):
    """Detects text in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    texts = image.detect_text()
    text = texts[0].description
    text = text.replace('\n', ' ').replace('\r',' ')
    print(text)

def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)

    texts = image.detect_text()
    text = texts[0].description
    text = text.replace('\n', ' ').replace('\r',' ')
    print(text)

# Instantiates a client
vision_client = vision.Client()
# detect_text('7.jpg')