""" module for the decorators in firmware """


from functools import wraps
from flask import render_template


def login_required(session=None):
    """function that calls the decorator with 1 parameter"""
    def login_decorator(funct):
        """ the actual deocrator that wraps a view function and renders it only
            if the conditions are met (user logged in as admin) """
        @wraps(funct)
        def check_login(*args, **kwargs):
            """ the new wrapped function with the conditions included """
            errors = dict()
            if session is None:
                errors['no_server'] = "Server not running at the moment!"
                return render_template('404.html', error_messages=errors)
            if session.get('user', None) is None:
                errors['not_logged'] = "You must be logged in to access this page"
                return render_template('404.html', error_messages=errors)
            if session['user'].get('privilege', 'user') == 'user':
                errors['not_logged_admin'] = "You must be logged in as an admin \
                    to access this page.Please upgrade to admin"
                return render_template('404.html', error_messages=errors)
            return funct(*args, **kwargs)
        return check_login
    return login_decorator
