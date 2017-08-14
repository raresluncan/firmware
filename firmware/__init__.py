import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import pdb

app=Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'firmware.db'),
    SECRET_KEY = 'key'
))

from firmware import views
from firmware import repository
from firmware import uploaders
from firmware import validators
