import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort
from flask import render_template, flash, send_from_directory

from firmware import app
import pdb

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file(file, upload_name, upload_type):
    filename = "default.jpg"
    if file:
        filename_temp = upload_name + ".jpg"
        filename = file.filename
        folder = os.path.join(os.path.dirname(__file__), 'static', upload_type)
        file.save(os.path.join(folder, filename))
        os.rename(os.path.join(folder, filename), os.path.join(folder, filename_temp))
        filename = filename_temp
    return filename
