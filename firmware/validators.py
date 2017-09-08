"""Validators - functions to validate stuff"""

from firmware.repository import get_company, get_username_by_id


def validate_user_type(current_session, company_id):
    """ checks if the user who wants to edit a company is the \
       user who added it """
    errors = dict()
    added_by_id = get_company(company_id).added_by_id
    added_by_username = get_username_by_id(added_by_id)
    if current_session['user'].get('username', None) != added_by_username:
        errors['stranger'] = ("Only the author, %s, can edit this company!" %
                              added_by_username)
    return errors


def validate_add_company(current_session, company_id):
    """ checks if the user has privilege to add a company """
    errors = dict()
    if not current_session.get('logged_in', None):
        errors['logged_in'] = "You must be logged in to add a company!"
        return errors
    if current_session['user'].get('privilege', None) != 'admin':
        errors['not_admin'] = ("Sorry, dear %s.Only admins can add or edit \
                               companies.Please upgrade to admin."
                               % current_session['user'].get('username', None))
        return errors
    if company_id is not None:
        errors = validate_user_type(current_session, company_id)
        return errors


def validate_add_user(current_session):
    """ checks if user has privilege to add a new user """
    errors = dict()
    if not current_session.get('logged_in', None):
        errors['logged_in'] = "You must be logged in to add a user!"
        return errors
    if current_session['user'].get('privilege', None) != 'admin':
        errors['not_admin'] = "Sorry, dear %s.Only admins can add users.\
        Please upgrade to admin." % current_session['user'].get('username', None)
    return errors


def validate_company(company):
    """ checks if the user entered valid data when adding a company"""
    errors = dict()
    if company['name'] == "":
        errors['add-name'] = "Please add a name for your company!"
    if company['adress'] == "":
        errors['add-adress'] = "Please add an adress for your company!"
    if company['description'] == "":
        errors['add-description'] = "Please add a short description for \
        your company!"
    if company.get('category_id') is None:
        errors['add-category'] = 'Please select a category for your \
        company!'
    if company['details'] == "":
        errors['add-details'] = "Please add a few details about your \
        company!"
    return errors


def validate_new_user(user):
    """ checks if the user enterd valid data when adding a new user """
    errors = dict()
    if user['username'] == "":
        errors['username'] = "Please add a username"
    if user['password'] == "":
        errors['password'] = "Please add a password"
    if user['confirm_password'] != user['password']:
        errors['confirm_password'] = "Passwords don't match"
    if user['confirm_password'] == "":
        errors['confirm_password'] = "Please confirm your password!"
    if user['email'] == "":
        errors['email'] = "Please enter an email!"
    return errors


def validate_login(login):
    """ checks if good credentials were added at ay log-in attempt"""
    errors = dict()
    if login['username-login'] == "":
        errors['username-login'] = "Please enter your username"
    if login['password-login'] == "":
        errors['password-login'] = "Please enter your password"
    return errors


def validate_review(review):
    """ checks if user submitted a valid review """
    errors = dict()
    if review['review'] == "":
        errors['text'] = "Please write a review before submitting"
    return errors
