import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from uploaders import upload_file
from firmware import app

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'], timeout=1)
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print("Firmware initialized database sucessfully!")


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
    cur = db.execute("select * from companies")
    companies = cur.fetchall()
    return companies


def add_company(request_form,request_files):
    db = get_db()
    add_cursor = db.execute("select id from categories where \
        type='%s'" % str(request_form.get('select-category-list')))
    category_id = add_cursor.fetchall()[0]
    db.execute("insert into companies (name, \
        description , details, rating, \
        logo, adress, category_id) values \
        (?, ?, ?, ?, ?, ?, ?)", (request_form['company_name'],
        request_form['company_description'],
        request_form['company_details'],
        0, upload_file(request_files['company_logo'])+".jpg",
        request_form['company_adress'],
        str(int(category_id[0]))))
    db.commit()
    add_cursor = db.execute("select MAX(id) from companies")
    new_company_id = add_cursor.fetchall()[0]
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
    categoryCursors = db.execute( 'select type from categories where \
    id="%s"' % get_company(company_id)['category_id'])
    category = categoryCursors.fetchall()
    return category[0]['type']


def get_reviews(company_id):
    db = get_db()
    reviewsCursor = db.execute(
        'select user_id, review from reviews where company_id="%s" order by id \
        desc' % company_id
    )
    reviews = reviewsCursor.fetchall()
    return reviews
