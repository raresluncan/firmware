# coding: utf8
""" Routes for app paths and functions combining multiple modules """

import json
import sqlalchemy.orm
from flask import request, session, render_template, redirect
from firmware import app
from firmware import repository
from firmware.models import Company, User, Review
from firmware.uploaders import upload_base64_file
from firmware.forms import AddUser, AddCompany, LogIn, AddReview
from firmware.decorators import login_required
from firmware.authorization import authorize_edit_company
from firmware import encrypt
from firmware.helper_functions import dict_to_multidict


def get_details(company_id):
    """get details about a company via it's id"""
    try:
        company = repository.get_company(company_id)
    except sqlalchemy.orm.exc.NoResultFound:
        errors = {'company-not-found': "Company not found!"}
        return render_template('404.html', error_messages=errors)
    category = company.category.domain
    reviews = repository.get_reviews(company_id)
    added_by_user = company.added_by_user.username
    return company, category, reviews, added_by_user


@app.route('/home')
def home():
    """ function called when home path (url) is accessed"""
    category = request.args.get('category', 'all categories')
    if category == 'all categories':
        companies = repository.get_companies()
    else:
        companies = repository.get_filtered_companies(category)
    return render_template('index.html', companies=companies,
                           categories=repository.get_categories(),
                           current_category=category)


@app.route('/404-page-not-found')
def not_found(errors):
    """ function to render page for error 404 """
    return render_template('404.html', error_messages=errors)


@app.route('/details/<company_id>', methods=['GET'])
def details(company_id):
    """ function to show details about a company via it's id """
    try:
        company, category, reviews, added_by_user = get_details(company_id)
        add_review_form = AddReview()
    except ValueError:
        errors = dict()
        errors['Company-not-found'] = "Company not found!"
        return render_template('404.html', error_messages=errors)

    return render_template('details.html', reviews=reviews,
                           add_review_form=add_review_form, company=company,
                           category=category, added_by_user=added_by_user)


@app.route('/add-review/<company_id>', methods=['POST'])
@login_required('user', method='POST')
def add_review(company_id):
    """ function to add a review when user clicks submit """
    review_data = dict_to_multidict(request.json)
    add_review_form = AddReview(review_data)
    if add_review_form.validate():
        review = Review(user_id=session['user']['id'],
                        company_id=company_id, rating=0,
                        **add_review_form.to_dict())
        repository.add_review(review)
        response = {
            'success': True,
            'data': review.to_dict(),
            'user': session.get('user', "no-user-error")
        }
        return json.dumps(response)
    response = {
        'success': False,
        'errors': add_review_form.errors
    }
    return json.dumps(response)


@app.route('/company/', defaults={'company_id': None}, methods=['GET', 'POST'])
@app.route('/company/<company_id>', methods=['GET', 'POST'])
@login_required('admin')
def add_company(company_id):
    """ function called when an admin wants to add a new company or edit \
        one of it's own """
    categories = repository.get_categories()
    if company_id:
        try:
            company = repository.get_company(company_id)
            add_new_company_form = AddCompany(obj=company,
                                              categories=categories)
            add_new_company_form.submit.label.text = "SAVE CHANGES"
            errors = authorize_edit_company(session, company)
            if errors:
                return render_template('404.html', error_messages=errors)
        except sqlalchemy.orm.exc.NoResultFound:
            errors = dict()
            errors['404'] = "Company does not exist!"
            return render_template('404.html', error_messages=errors)
    else:
        add_new_company_form = AddCompany(categories=categories)
    return render_template('add_company.html',
                           categories=categories, company_id=company_id,
                           add_company_form=add_new_company_form,
                           errors=add_new_company_form.errors)


@app.route('/company/add/', defaults={'company_id': None}, methods=['POST'])
@app.route('/company/add/<company_id>', methods=['POST'])
@login_required('admin', method='POST')
def add_new_company(company_id):
    """ route for AJAX post request from client
        adds a company to the database if request data is valid"""
    company_data = dict_to_multidict(request.json)
    add_new_company_form = AddCompany(company_data)
    if add_new_company_form.validate():
        logo = upload_base64_file(request.json.get('picture', None),
                                  request.json.get('name'),
                                  'Images')
        add_new_company_form.logo.data = logo
        if company_id is None:
            company = Company(added_by_id=session['user']['id'],
                              **add_new_company_form.to_dict())
            added_company = repository.add_company(company)
            added_company_dict = added_company.to_dict()
            added_company_dict['flash'] = "add"
            del added_company_dict['added_by_user']
            response = {
                'success': True,
                'data': added_company_dict,
                'user': session.get('user', "no-user-error")
            }
            return json.dumps(response)
        updated_company = repository.update_company(add_new_company_form.to_dict(),
                                                    company_id)
        updated_company_dict = updated_company.to_dict()
        updated_company_dict['flash'] = "update"
        del updated_company_dict['added_by_user']
        response = {
            'success': True,
            'data': updated_company_dict,
            'user': session.get('user', "no-user-error")
        }
        return json.dumps(response)
    response = {
        'success': False,
        'errors': add_new_company_form.errors
    }
    return json.dumps(response)


@app.route('/user/new', methods=['GET', 'POST'])
@login_required('admin')
def add_user():
    """ function called ONLY when an ADMIN wants to add a new user """
    add_user_form = AddUser()
    return render_template('add_user.html', add_user_form=add_user_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ view to render the form for logging in """
    login_form = LogIn()
    if session.get('user', None) is not None:
        errors = dict()
        errors['user'] = "You are already logged in.Please log out before \
            trying to log in again"
        return render_template('404.html', error_messages=errors)
    return render_template('login.html', data=request.form,
                           session=session, login_form=login_form)


@app.route('/login/request', methods=['POST'])
def login_request():
    """ route for the AJAX post request for logging in
        logs a user in if data is valid """
    login_data = dict_to_multidict(request.json)
    login_form = LogIn(login_data)
    if session.get('user', None) is not None:
        errors = {
            'already-logged': "An account is already logged in"
        }
        response = {
            'success': False,
            'errors': errors
        }
    if login_form.validate():
        if repository.check_user(login_form.username.data,
                                 login_form.password.data) is False:
            errors = {
                'invalid': "Invalid credentials!Please check your username and \
                    password again!"
            }
            response = {
                'success': False,
                'errors': errors
            }
            return json.dumps(response)
        user = repository.get_user(login_form.username.data).serialize()
        session['logged_in'] = True
        session['user'] = user
        response = {
            'success': True,
            'data': user,
            'user': user
        }
        return json.dumps(response)
    response = {
        'success': False,
        'errors': login_form.errors
    }
    return json.dumps(response)


@app.route('/user/add', methods=['POST'])
@login_required('admin', method='POST')
def add_new_user():
    """ route for the AJAX post request
        adds a user to database if data from the request is valid """
    new_user_data = dict_to_multidict(request.json)
    add_user_form = AddUser(new_user_data)
    if add_user_form.validate():
        add_user_form.password.data = encrypt.generate_password_hash(
            add_user_form.password.data
        )
        user = User(avatar=upload_base64_file(request.json.get('picture', None),
                                              request.json['username'],
                                              "Avatars"),
                    **add_user_form.to_dict())
        new_user = repository.add_user(user)
        response = {
            'success': True,
            'data': new_user.to_dict(),
            'user': session.get('user', "no-user-error")
        }
        return json.dumps(response)
    response = {
        'success': False,
        'errors': add_user_form.errors
    }
    return json.dumps(response)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    """ route acessed when log-out button is clicked """
    errors = dict()
    session['logged_in'] = False
    if session.get('user', None) is None:
        errors['not_logged'] = "You must be logged in to log out"
        return render_template("404.html", error_messages=errors)
    session.pop('user')
    return redirect("/home#reload-point")
