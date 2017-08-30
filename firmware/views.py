import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from firmware import app
import repository
from validators import validate_company, validate_user, validate_login, validate_review

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
    return render_template('index.html', companies=repository.get_companies())


@app.route('/404-page-not-found')
def not_found(error):
    return render_template('404.html', error_message=error)


@app.route('/details/<company_id>')
def details(company_id):
    company, category, reviews = get_details(company_id)
    return render_template('details.html', reviews=reviews, company=company,
        category=category)


@app.route('/add/company/', methods=['GET', 'POST'])
def add_company():
    categories = repository.get_categories()
    errors = dict()
    error_point=''
    if request.method == 'POST':
        errors = validate_company(request.form, request.files)
        if not errors:
            new_company_id = repository.add_company(request.form, request.files)
            flash('Congratulations on adding your company, ' \
                + request.form['company_name']+' to our website!Check out your \
                 profile below.')
            return redirect(url_for('details', company_id=new_company_id))
    return render_template('add_company.html', data=request.form, errors=errors,
        categories=categories)


@app.route('/add/user/', methods=['GET', 'POST'])
def add_user():
    errors = dict()
    if request.method == 'POST':
        errors = validate_user(request.form, request.files)
        if not errors:
            new_user_id = repository.add_user(request.form, request.files)
            flash("NEW USER ADDED SUCESFULLY!")
            return redirect(url_for('home'))
    return render_template('add_user.html', data=request.form, errors=errors)


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
            return render_template('index.html', user=user, companies=
                repository.get_companies())
    return render_template('login.html', errors=errors, data=request.form)


@app.route('/logout')
def logout():
    session['logged_in'] = False;
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
