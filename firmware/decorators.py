""" module for the decorators in firmware """

import json
from functools import wraps
from flask import render_template
from firmware.views import session


def login_required(role, method="GET"):
    """function that calls the view decorator with 1 parameter"""
    def view_decorator(funct):
        """ the actual deocrator that wraps a view function and renders it only
            if the conditions are met:
                - if the role is "user" the decorator checks if a user with
                the privilege of 'user' is logged in
                - if the role is "admin" the decorators checks if a user with
                the privilege of 'admin' is logged in"""
        @wraps(funct)
        def check_login(*args, **kwargs):
            """ the new wrapped function with the conditions included """
            if session is None:
                errors = {'no_server': "Server not running at the moment!"}
                return render_template('404.html', error_messages=errors)
            if session.get('user', None) is None:
                errors = {'not_logged': "You must be logged in to continue"}
                if method == "GET":
                    return render_template('404.html', error_messages=errors)
                response = {
                    'success': False,
                    'errors': errors
                }
                return json.dumps(response)
            if role == 'admin' and session['user'].get('privilege', 'user') == 'user':
                errors = {'not_logged_admin': "You must be logged in as an admin \
                to access this page.Please upgrade to admin"}
                return render_template('404.html', error_messages=errors)
            return funct(*args, **kwargs)
        return check_login
    return view_decorator
