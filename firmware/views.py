import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from firmware import app
import repository
from validators import validate_company, validate_user, validate_login, validate_review, validate_add_company
from validators import validate_add_user

import pdb


def get_details(company_id):
    company = repository.get_company(company_id)
    if company == None:
        return render_template('404.html', error_message="Company not found!")
    category = repository.get_category(company_id)
    reviews = repository.get_reviews(company_id)
    return company, category, reviews


@app.route('/home')
def home():
    category = request.args.get('category', 'all categories')
    if category == 'all categories':
        companies = repository.get_companies()
    else:
        companies = repository.get_filtered_companies(category)
    return render_template('index.html', companies=companies,
        categories=repository.get_categories(), current_category=category)


@app.route('/404-page-not-found')
def not_found(error):
    return render_template('404.html', error_message=error)


@app.route('/details/<company_id>')
def details(company_id):
    try:
        company, category, reviews = get_details(company_id)
    except ValueError:
        return render_template('404.html', error_message="Company not found!")
    return render_template('details.html', reviews=reviews, company=company,
        category=category)


@app.route('/add/company/', methods=['GET', 'POST'])
def add_company():
    errors = validate_add_company(session)
    categories = repository.get_categories()
    if not errors:
        errors = dict()
        if request.method == 'POST':
            errors = validate_company(request.form, request.files)
            if not errors:
                new_company_id = repository.add_company(request.form,
                    request.files, session.get('username', None))
                flash('Congratulations on adding your company, ' \
                    + request.form['company_name']+' to our website!Check out your \
                     profile below.')
                return redirect(url_for('details', company_id=new_company_id))
        return render_template('add_company.html', data=request.form, errors=errors,
            categories=categories)
    else:
        return render_template('404.html', error_message="Oops!You cannot add a\
            company unless you are logged in and your account is an admin!")


@app.route('/add/user/', methods=['GET', 'POST'])
def add_user():
    errors = dict()
    errors = validate_add_user(session)
    if not errors:
        if request.method == 'POST':
            errors = validate_user(request.form, request.files)
            if not errors:
                new_user_id = repository.add_user(request.form, request.files)
                flash("NEW USER ADDED SUCESFULLY!")
                category = request.args.get('category', 'all categories')
                return redirect(url_for('home', current_category = request.args.get('category', 'all categories')))
        return render_template('add_user.html', data=request.form, errors=errors)
    else:
        return render_template('404.html', error_message="Only admins can add other\
            users! Please log in as an admin to add an account!")


@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = dict()
    if request.method == 'POST':
        errors = validate_login(request.form)
        if repository.check_user(request.form['username-login'],
            request.form['password-login']) == 0:
                errors['invalid'] = "Please enter valid credentials!"
        if not errors:
            user = dict()
            session['logged_in'] = True
            flash('Welcome back, dear %s!' % request.form['username-login'])
            session['username'] = request.form['username-login']
            session['avatar'] = repository.get_avatar(session['username'])
            session['privilege'] = repository.get_privilege(session['username'])
            return render_template('index.html', user=user, companies=
                repository.get_companies(),
                categories=repository.get_categories())
    return render_template('login.html', errors=errors, data=request.form,
        session=session)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    session.pop('avatar', None)
    flash('You were logged out')
    return redirect(url_for('home'))


@app.route('/add_review/<company_id>', methods=['GET', 'POST'])
def add_review(company_id):
    if request.method == "POST":
        errors = dict()
        if session.get('logged_in', None):
            errors = validate_review(request.form)
            if not errors:
                repository.add_reviews(company_id, session['username'],request.form['enter-review'])
                flash("Review added sucessfully")
                return redirect(url_for('details', company_id=company_id))
        else:
            errors['not_logged'] = "You must be logged in to review a company!"
    company, category, reviews = get_details(company_id)
    return render_template('details.html', reviews=reviews, company=company,
        category=category, errors=errors)
