from flask import Flask, request
import boto
from SimpleCV import Image, Camera
import time
from boto.s3.key import Key
import uuid

app = Flask(__name__)
app.config.from_object('config')

lastUploadedFile = 0

def get_image_name():
    #return image name as currenttime.jpg
    epoch_time = int(time.time())
    return epoch_time + ".jpg"


def take_photo(fileName=0):
    if(fileName == 0):
        return fileName
    cam = Camera()
    img = cam.getImage()
    img.save(fileName)
    return fileName

@app.route('/img', methods=['POST', 'GET'])
def upload_img():
    if(request.method == 'POST' 
            and request.form["key"] == app.config["AUTH_KEY"]):
        
        # Create connection to Amazon S3
        s3 = boto.s3.connect_s3(app.config["S3_KEY"], app.config["S3_SECRET"])

        # Create a link to the bucket.
        bucket = s3.get_bucket(app.config["S3_BUCKET"])

        # A unique ID representing the photot
        fileId = uuid4().hex

        # The file name
        fileName = fileId + '.jpeg'
        
        # File address
        fileNameWithDir = app.config["S3_UPLOAD_DIRECTORY"] + "/" + fileName  

        #  This is where it calls a function to take a photo using the webcam
        img_file = take_photo(fileName)
        
        # Default
        toReturn = "IMG_ERROR"


        if img_file != None:
            k = Key(bucket)
            k.key = img_file
            k.set_contents_from_filename(img_file)
            toReturn = fileNameWithDir

        return str(fileNameWithDir)

    return "AUTH_ERROR"



if __name__ == '__main__':
    app.run()
