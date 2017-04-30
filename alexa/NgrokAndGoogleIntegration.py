from __future__ import print_function

import json
import urllib
import boto3
import urllib
import urllib2
import os


endpoint_url = "https://omh5gu7ow3.execute-api.us-east-2.amazonaws.com/dev/processmessage"
def getImageText(url):


    try:
        data = {"inputMessage": {
                    "Url": url
            }
        }

        headers = {"Content-Type": "application/json"
        }
        
        request = urllib2.Request(endpoint_url, data = json.dumps(data), headers = headers)
        response = urllib2.urlopen(request)
        
        print('Response text: {} \nResponse status: {}'.format(response.read(), response.getcode()))

        return response.read()
    except Exception as e:
        print(e)

# Calls the laptop using ngrok and then 
# Returns: a URL to the photo in S3.
def getPhoto():
    try:
        
        data = {"inputMessage": {
                    "key": os.environ["NGROK_AUTH_KEY"]
            }
        }

        headers = {"Content-Type": "application/json",
        }
        # Invoke Cloud Endpoints API
        request = urllib2.Request(os.environ["NGROK_URL"], data = json.dumps(data), headers = headers)
        response = urllib2.urlopen(request)
        
        print(response.read())
        return response.read()
        
    except Exception as e:
        print(e)
        print('Error in retrieving image from computer')
        raise e

def lambda_handler(event, context):
    return getImageText(getPhoto())