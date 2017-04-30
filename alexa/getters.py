import os
import 

# Doing this because there's also a "request" object in flask ask
import requests

def sendToGoogle(url):

    try:
        data = {"inputMessage": {
            "Url": url
            }
        }

        headers = {"Content-Type": "application/json",
            "x-api-key": os.environ["ENDPOINT_KEY"]
        }

        googleReply = requests.post(os.environ["ENDPOINT_URL"], 
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
        photoUrl = requests.get(
                os.environ["NGROK_URL"], 
                { 'key': os.environ["NGROK_AUTH_KEY"] })
        return photoUrl.text
    except Exception as e:
        print(e)
        print('Error in retrieving image from computer')
        raise e
    

