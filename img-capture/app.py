from flask import Flask, render_template, flash
import boto
from boto.s3.key import Key
import uuid

app = Flask(__name__)
app.config.from_object('config')

lastUploadedFile = 0

def take_photo(fileName=0):
    return 

@app.route('/img', methods=['POST', 'GET'])
def upload_img():
    if request.method == 'POST':
        
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
        toReturn = "ERROR"


        if img_file != None:
            k = Key(bucket)
            k.key = img_file
            k.set_contents_from_filename(img_file)
            toReturn = fileNameWithDir

        return str(fileNameWithDir)

    return "ERROR"



if __name__ == '__main__':
    app.run()