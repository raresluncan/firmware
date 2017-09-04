import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from uploaders import upload_file
from firmware import app

import pdb


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'], timeout=1)
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_companies():
    db = get_db()
    get_companies_query = db.execute("select * from companies")
    companies = get_companies_query.fetchall()
    return companies


def add_company(company, company_files, username):
    db = get_db()
    db.execute("insert into companies (name, \
        description , details, rating, \
        logo, adress, category_id, added_by) values \
        (?, ?, ?, ?, ?, ?, ?, ?)", (company['company_name'],
        company['company_description'],
        company['company_details'],
        0, upload_file(company_files['company_logo'],
        company['company_name'], 'Images'),
        company['company_adress'],
        company.get('select-category-list'),
        username))
    db.commit()
    new_company_id_query = db.execute("select MAX(id) from companies")
    new_company_id = new_company_id_query.fetchall()[0]
    return new_company_id[0]


def get_company(company_id):
    db = get_db()
    query = 'select * from companies where id="%s"' % company_id
    records = db.execute(query).fetchmany(1)
    if len(records) == 0:
        return None
    return records[0];


def get_category(company_id):
    db = get_db()
    category_query = db.execute('select type from categories where \
    id = "%s"' % get_company(company_id)['category_id'])
    category = category_query.fetchall()
    return category[0]['type']


def get_categories():
    db = get_db()
    categories_query = db.execute('select * from categories')
    categories = categories_query.fetchall()
    return categories


def get_reviews(company_id):
    db = get_db()
    reviews_query = db.execute(
        'select users.username, users.avatar, reviews.id, reviews.user_id,\
        reviews.review from reviews inner join users on \
        reviews.user_id = users.id where reviews.company_id = "%s" order by \
        reviews.id desc'
        % company_id
    )
    reviews = reviews_query.fetchall()
    return reviews


def add_user(user, user_files):
    db = get_db()
    add_user_query = db.execute("insert into users (username, password , email, \
        name, surname, avatar, contact, privilege, gender) values \
        (?, ?, ?, ?, ?, ?, ?, ?, ?)", (user['username'],
        user['password'],
        user['email'],
        user.get('real_name', '-'),
        user['surname'],
        upload_file(user_files['user_avatar'] ,
            user['username'], 'Avatars'),
        user['contact'],
        user['radio-group-privilege'],
        user['radio-group-gender'])
        )
    db.commit()
    return True


def check_user(username, password):
    db = get_db()
    errors = dict()
    check_user_query = db.execute("select username, password from users where \
        username=? and password=?", (username, password))
    compatible_user = check_user_query.fetchmany()
    if not compatible_user:
        return 0
    return 1


def get_avatar(username):
    db = get_db()
    get_user_query = db.execute("select avatar from users where username = '%s'"
        % username )
    user = get_user_query.fetchmany()
    avatar = user[0]['avatar']
    return avatar

def get_privilege(username):
    db = get_db()
    get_privilege_query = db.execute("select privilege from users where \
        username = '%s'" % username )
    privilege_row = get_privilege_query.fetchmany()
    privilege = privilege_row[0]['privilege']
    return privilege


def add_reviews(company_id, user, text):
    db = get_db()
    get_user_id_query = db.execute("select id from users where username='%s'"
        % user)
    user_id_row = get_user_id_query.fetchmany()
    user_id = user_id_row[0]['id']
    add_review_query = db.execute("insert into reviews (user_id, review, \
    company_id) values (?, ?, ?)", (user_id,text,company_id))
    db.commit()
    return None


def get_category_id(category):
    db = get_db()
    get_category_id_query = db.execute("select id from categories where \
        type = '%s'" % category)
    category_id_row = get_category_id_query.fetchmany()
    category_id = category_id_row[0]['id']
    return category_id


def get_filtered_companies(category):
    db = get_db()
    category_id = get_category_id(category)
    get_companies_query = db.execute("select * from companies where \
        category_id = '%s'" % category_id)
    companies = get_companies_query.fetchall()
    return companies
