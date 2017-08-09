import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from firmware import app
from repository import get_companies,get_category,get_reviews
from validators import validate_company


@app.route('/home')
def home():
    return render_template('index.html', companies=get_companies())


@app.route('/404-page-not-found')
def not_found(error):
    return render_template('404.html', error_message=error)


@app.route('/details/<company_id>')
def details(company_id):
    company = get_company(company_id)
    if(company == None)
        return render_template('404.html', error_message="Company not found!")
    category = get_category(company_id)
    reviews = get reviews(company_id)
    return render_template('details.html', reviews=reviews, company=company,
        category=category)


@app.route('/add/company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        errors = validate_company(request.form, request.files)
        if not errors:
            new_company_id = add_company(request.form)
            flash('Congratulations on adding your company, ' \
                + request.form['company_name']+' to our website!Check out your \
                 profile below.')
            return redirect(url_for('details', company_id=new_company_id))
    return render_template('add_company.html', data=request.form, errors=errors)
