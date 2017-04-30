import io
from google.cloud import vision

def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.     """
    vision_client = vision.Client()
    image = vision_client.image(source_uri=uri)
    texts = image.detect_text()
    text = texts[0].description
    text = text.replace('\n', ' ').replace('\r',' ')
    return text

print(detect_text_uri("https://about.canva.com/wp-content/uploads/sites/3/2015/01/business_bookcover.png"))
