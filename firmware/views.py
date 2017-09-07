""" Routes for app paths and functions combining multiple modules """

from flask import request, session, redirect, url_for, render_template, flash

from firmware import app
from firmware import repository
from firmware.validators import validate_company, validate_new_user
from firmware.validators import validate_login, validate_review
from firmware.validators import validate_add_company, validate_add_user
from firmware.models import Company, User, Review, Category

import pdb


def get_details(company_id):
    """get details about a company via it's id"""
    company = repository.get_company(company_id)
    if company is None:
        errors = dict()
        errors['company-not-found'] = "Company not found!"
        return render_template('404.html', error_messages=errors)
    category = repository.get_category(company_id)
    reviews = repository.get_reviews(company_id)
    added_by_user = repository.get_username_by_id(company.added_by_id)
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


@app.route('/details/<company_id>')
def details(company_id):
    """ function to show details about a company via it's id """
    try:
        company, category, reviews, added_by_user = get_details(company_id)
    except ValueError:
        errors = dict()
        errors['Company-not-found'] = "Company not found!"
        return render_template('404.html', error_messages=errors)
    return render_template('details.html', reviews=reviews, company=company,
                           category=category, added_by_user=added_by_user)


@app.route('/company/', defaults={'company_id': None}, methods=['GET', 'POST'])
@app.route('/company/<company_id>', methods=['GET', 'POST'])
def add_company(company_id):
    """ function called when an admin wants to add a new company or edit \
        one of it's own """
    errors = validate_add_company(session, company_id)
    categories = repository.get_categories()
    data = dict()
    if company_id:
        button_text = "SAVE CHANGES"
        try:
            data = repository.fragment_company(company_id)
        except TypeError:
            errors = dict()
            errors['404'] = "Company does not exist!"
            return render_template('404.html', error_messages=errors)
    else:
        data = request.form.to_dict()
        button_text = "SUBMIT COMPANY"
    if not errors:
        errors = dict()
        if request.method == 'POST':
            errors = validate_company(request.form)
            if not errors:
                if company_id is None:
                    company = Company(added_by_id=session['user']['id'], **request.form.to_dict())
                    new_company_id = repository.add_company(company,
                                                            request.files)
                    flash('Congratulations on adding your company, ' \
                        + company.name +' to our website!Check out \
                        your profile below.')
                    return redirect(url_for('details',
                                            company_id=new_company_id))
                if not errors:
                    updated_company = Company(**request.form.to_dict())
                    repository.update_company(updated_company, request.files,
                                              company_id)
                    flash('Your company has been updated!')
                    return redirect(url_for('details', company_id=company_id))
                return render_template('404.html', error_messages=errors)
        if request.form.get('category') is not None:
            data['category'] = \
                repository.get_category_by_id(request.form.get('category'))
        return render_template('add_company.html', data=data, errors=errors,
                               categories=categories, button_text=button_text,
                               company_id=company_id)
    else:
        return render_template('404.html', error_messages=errors)


@app.route('/add/user/', methods=['GET', 'POST'])
def add_user():
    """ function called when an admin wants to add a new user """
    errors = dict()
    errors = validate_add_user(session)
    if not errors:
        if request.method == 'POST':
            errors = validate_new_user(request.form)
            if not errors:
                user = User(**request.form.to_dict())
                new_user_id, username = repository.add_user(user, request.files)
                flash("NEW USER, %s, ADDED SUCESFULLY!" % username)
                return redirect(url_for('home', current_category=\
                                        request.args.get('category', \
                                        'all categories')))
        return render_template('add_user.html', data=request.form, errors=errors)
    else:
        return render_template('404.html', error_messages=errors)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ function called when an anon user wants to log in"""
    errors = dict()
    if request.method == 'POST':
        errors = validate_login(request.form)
        if repository.check_user(request.form['username-login'],
                                 request.form['password-login']) == 0:
            errors['invalid'] = "Please enter valid credentials!"
        if not errors:
            user = repository.get_user(request.form['username-login'])
            session['logged_in'] = True
            session['user'] = user
            flash('Welcome back, dear %s!' % user['username'])
            return render_template('index.html', user=user, companies=
                                   repository.get_companies(),
                                   categories=repository.get_categories())
    return render_template('login.html', errors=errors, data=request.form,
                           session=session)


@app.route('/logout')
def logout():
    """ route acessed when log-out button is clicked """
    session['logged_in'] = False
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('home'))


@app.route('/add_review/<company_id>', methods=['GET', 'POST'])
def add_review(company_id):
    """ function called when a user tries to submit a review"""
    if request.method == "POST":
        errors = dict()
        if session.get('logged_in', None):
            errors = validate_review(request.form)
            if not errors:
                review = Review(user_id = session['user']['id'],
                                company_id = company_id,
                                **request.form.to_dict())
                repository.add_reviews(review)
                flash("Review added sucessfully")
                return redirect(url_for('details', company_id=company_id))
        else:
            errors['not_logged'] = "You must be logged in to review a company!"
    company, category, reviews, added_by_user = get_details(company_id)
    return render_template('details.html', reviews=reviews, company=company,
                           category=category, errors=errors,
                           added_by_user=added_by_user)
