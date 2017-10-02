"""UPLOADERS - function to upload files to server"""

import os
import base64


def upload_base64_file(info, filename, foldername):
    """ decodes an image from base64 format to File """
    if not info:
        return "default.jpg"
    folder = os.path.join(os.path.dirname(__file__), 'static', foldername)
    imgdata = base64.b64decode(info.split(",")[1])
    with open(folder+"/"+filename+".jpg", 'wb') as new_file:
        new_file.write(imgdata)
    return filename+".jpg"
