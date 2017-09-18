# coding: utf8
""" Routes for app paths and functions combining multiple modules """


import sqlalchemy.orm
from flask import request, session, redirect, url_for, render_template, flash
from firmware import app
from firmware import repository
from firmware.models import Company, User, Review
from firmware.uploaders import upload_file
from firmware.forms import AddUser, AddCompany, LogIn, AddReview
from firmware.decorators import login_required
from firmware.authorization import authorize_edit_company



def get_details(company_id):
    """get details about a company via it's id"""
    try:
        company = repository.get_company(company_id)
    except sqlalchemy.orm.exc.NoResultFound:
        errors = dict()
        errors['company-not-found'] = "Company not found!"
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


@app.route('/details/<company_id>', methods=['GET', 'POST'])
def details(company_id):
    """ function to show details about a company via it's id """
    errors = dict()
    try:
        company, category, reviews, added_by_user = get_details(company_id)
        add_review_form = AddReview(request.form)
    except ValueError:
        errors['Company-not-found'] = "Company not found!"
        return render_template('404.html', error_messages=errors)
    if request.method == 'POST' and add_review_form.validate():
        if session.get('logged_in', False) is True:
            review = Review(user_id=session['user']['id'],
                            company_id=company_id,
                            **add_review_form.to_dict())
            repository.add_review(review)
            flash("Review added sucessfully")
            return redirect(url_for('details', company_id=company_id))
        errors['logged_in'] = "You must be logged in to add a review!"
    errors.update(add_review_form.errors)
    return render_template('details.html', reviews=reviews,
                           add_review_form=add_review_form, company=company,
                           category=category, added_by_user=added_by_user,
                           errors=errors)


@app.route('/company/', defaults={'company_id': None}, methods=['GET', 'POST'])
@app.route('/company/<company_id>', methods=['GET', 'POST'])
@login_required(session)
def add_company(company_id):
    """ function called when an admin wants to add a new company or edit \
        one of it's own """

    categories = repository.get_categories()
    if company_id and request.method == 'GET':
        try:
            company = repository.get_company(company_id)
            errors = authorize_edit_company(session, company)
            if errors:
                return render_template('404.html', error_messages=errors)
            add_new_company_form = AddCompany(obj=company,
                                              categories=categories)
            add_new_company_form.submit.label.text = "SAVE CHANGES"
        except sqlalchemy.orm.exc.NoResultFound:
            errors = dict()
            errors['404'] = "Company does not exist!"
            return render_template('404.html', error_messages=errors)
    else:
        add_new_company_form = AddCompany(request.form, categories=categories)

    if request.method == 'POST' and add_new_company_form.validate():
        if company_id is None:
            logo = upload_file(request.files['logo'],
                               add_new_company_form.name.data,
                               "Images")
            add_new_company_form.logo.data = logo
            company = Company(added_by_id=session['user']['id'],
                              **add_new_company_form.to_dict())
            new_company_id = repository.add_company(company).id
            flash('Congratulations on adding your company, ' \
                + company.name +' to our website!Check out \
                your profile below.')
            return redirect(url_for('details',
                                    company_id=new_company_id))
        updated_company_id = repository.update_company(request.form.to_dict(),
                                                       company_id).id
        flash('Your company has been updated!')
        return redirect(url_for('details',
                                company_id=updated_company_id))

    return render_template('add_company.html',
                           categories=categories, company_id=company_id,
                           add_company_form=add_new_company_form,
                           errors=add_new_company_form.errors)




@app.route('/add/user/', methods=['GET', 'POST'])
@login_required(session)
def add_user():
    """ function called ONLY when an ADMIN wants to add a new user """
    add_user_form = AddUser(request.form)
    if request.method == 'POST' and add_user_form.validate():
        user = User(avatar=upload_file(request.files['avatar'],
                                       add_user_form.username.data,
                                       "Avatars"),
                    **add_user_form.to_dict())
        new_user = repository.add_user(user)
        # print str(new_user_id) + "will be used when adding a new user page"
        flash("NEW USER, %s, ADDED SUCESFULLY!" % new_user.username)
        return redirect(url_for('home', current_category=\
                                request.args.get('category', \
                                'all categories')))
    return render_template('add_user.html',
                           errors=add_user_form.errors,
                           add_user_form=add_user_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ function called when an anon user wants to log in"""
    errors = dict()
    login_form = LogIn(request.form)
    if request.method == 'POST' and login_form.validate():
        if repository.check_user(login_form.username.data,
                                 login_form.password.data) is None:
            errors['invalid'] = "Invalid credentials!Please check your username \
                               and password again!"
        else:
            user = repository.get_user(login_form.username.data).serialize()
            session['logged_in'] = True
            session['user'] = user
            flash('Welcome back, dear %s!' % user['username'])
            return render_template('index.html', user=user,
                                   companies=repository.get_companies(),
                                   categories=repository.get_categories())

    errors.update(login_form.errors)
    return render_template('login.html', errors=errors, data=request.form,
                           session=session, login_form=login_form)


@app.route('/logout')
def logout():
    """ route acessed when log-out button is clicked """
    session['logged_in'] = False
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('home'))
