import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

import pdb

app=Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'firmware.db'),
    SECRET_KEY = 'such secret much wow so key no guess muh'
))


UPLOAD_FOLDER = 'static/Images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
filename="default"


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


@app.route('/home')
def home():
    db = get_db()
    cur = db.execute("select * from companies")
    companies = cur.fetchall()
    return render_template('index.html', companies=companies)


@app.route('/404-page-not-found')
def not_found(error):
    return render_template('404.html', error_message=error)


@app.route('/details/<company_id>')
def details(company_id):
    db = get_db()
    companyCursor = db.execute(
        'select * from companies where id="%s"' % company_id
    )
    records = companyCursor.fetchmany(1)
    if len(records) == 0:
        return render_template('404.html', error="The requested company \
        was not found!")
    categoryCursors = db.execute( 'select type from categories where \
    id="%s"' % records[0]['category_id'])
    category = categoryCursors.fetchall()
    reviewsCursor = db.execute(
        'select user, review from reviews where company_id="%s" order by id \
        desc' % company_id
    )
    reviews = reviewsCursor.fetchall()
    return render_template('details.html', reviews=reviews, company=records[0],
        category=category[0]['type'])


def upload_file(file):
    globals()['filename'] = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    os.rename(UPLOAD_FOLDER+filename, UPLOAD_FOLDER+filename+".jpg")


def validate_company(request_form, request_files):
    errors = dict()
    if(request_form['company_name'] == ""):
        errors['company_name'] = "Please add a name for your company!"
    if(request_form['company_adress'] == ""):
        errors['company_adress'] = "Please add an adress for your company!"
    if(request_form['company_description'] == ""):
        errors['company_description'] = "Please add a short description for \
        your company!"
    if request_form.get('select-category-list') == None:
        errors['select-category-list'] = 'Please select a category for your \
        company!'
    if(request_form['company_details'] == ""):
        errors['company_details'] = "Please add a few details about your \
        company!"
    file = request_files['company_logo']
    if file:
        upload_file(file)
    return errors


@app.route('/add/company', methods=['GET', 'POST'])
def add_company():
    db = get_db()
    errors = dict()
    if request.method == 'POST':
        errors = validate_company(request.form, request.files)
        if not errors:
            add_cursor = db.execute("select id from categories where \
                type='%s'" % str(request.form.get('select-category-list')))
            category_id = add_cursor.fetchall()[0]
            db.execute("insert into companies (name, \
                description , details, rating, \
                logo, adress, category_id) values \
                (?, ?, ?, ?, ?, ?, ?)", (request.form['company_name'],
                request.form['company_description'],
                request.form['company_details'],
                0, filename+".jpg",
                request.form['company_adress'],
                str(int(category_id[0]))))
            db.commit()
            add_cursor = db.execute("select MAX(id) from companies")
            new_company_id = add_cursor.fetchall()[0]
            flash('Congratulations on adding your company, ' \
                + request.form['company_name']+' to our website!Check out your \
                 profile below.')
            return redirect(url_for('details', company_id=new_company_id[0]))
    return render_template('add_company.html', data=request.form, errors=errors)
