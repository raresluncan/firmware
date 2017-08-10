import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from firmware import app

UPLOAD_FOLDER = 'firmware/static/Images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
filename="default"


def upload_file(file):
    if file:
        globals()['filename'] = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],globals()['filename']))
        os.rename(UPLOAD_FOLDER+filename, UPLOAD_FOLDER+filename+".jpg")
    return filename
