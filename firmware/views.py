import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from firmware import app
import repository
from validators import validate_company


@app.route('/home')
def home():
    return render_template('index.html', companies=repository.get_companies())


@app.route('/404-page-not-found')
def not_found(error):
    return render_template('404.html', error_message=error)


@app.route('/details/<company_id>')
def details(company_id):
    company = repository.get_company(company_id)
    if company == None:
        return render_template('404.html', error_message="Company not found!")
    category = repository.get_category(company_id)
    reviews = repository.get_reviews(company_id)
    return render_template('details.html', reviews=reviews, company=company,
        category=category)


@app.route('/add/company', methods=['GET', 'POST'])
def add_company():
    errors = dict()
    if request.method == 'POST':
        errors = validate_company(request.form, request.files)
        if not errors:
            new_company_id = repository.add_company(request.form, request.files)
            flash('Congratulations on adding your company, ' \
                + request.form['company_name']+' to our website!Check out your \
                 profile below.')
            return redirect(url_for('details', company_id=new_company_id))
    return render_template('add_company.html', data=request.form, errors=errors)
