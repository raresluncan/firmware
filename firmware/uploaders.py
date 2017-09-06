"""UPLOADERS - function to upload files locally"""

import os
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    """ allowed files that can be uploaded (not functioonal yet)"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file(new_file, upload_name, upload_type):
    """ uploads a file to the server """
    filename = "default.jpg"
    if new_file:
        filename_temp = upload_name + ".jpg"
        filename = new_file.filename
        folder = os.path.join(os.path.dirname(__file__), 'static', upload_type)
        new_file.save(os.path.join(folder, filename))
        os.rename(os.path.join(folder, filename), os.path.join(folder, filename_temp))
        filename = filename_temp
    return filename
