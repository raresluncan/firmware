"""Firmware module"""

import os
from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash
from flask.ext.bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'firmware.db'),
    SECRET_KEY='key'
))
encrypt = Bcrypt(app)


from firmware import views
from firmware import repository
from firmware import uploaders
from firmware import models
from firmware import database
from firmware import forms
from firmware import widgets
from firmware import decorators
from firmware import authorization
