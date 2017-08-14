import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from firmware import app
import pdb

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



def upload_file(file, path, upload_name):
    filename = "default.jpg"
    absolute_path = os.path.abspath("../"+path)
    if file:
        filename_temp = upload_name+".jpg"
        filename = file.filename
        pdb.set_trace()
        file.save(os.path.join(absolute_path,filename))
        os.rename(absolute_path+filename, absolute_path+filename_temp)
    return filename
