from SimpleCV import Image, Camera
import time

def get_image_name():
    #return image name as currenttime.jpg
    epoch_time = int(time.time())
    return str(epoch_time) + ".jpg"


def take_photo(fileName=0):
    if(fileName == 0):
        return fileName
    cam = Camera()
    img = cam.getImage()
    img.save(fileName)
    return fileName

take_photo(get_image_name())