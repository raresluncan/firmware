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
app.config['MY_MESSAGE'] = "error"


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
def not_found():
    return render_template('404.html', error_message=app.config['MY_MESSAGE'])


@app.route('/details/<company_id>')
def details(company_id):
    db = get_db()
    companyCursor = db.execute(
        'select * from companies where company_id="%s"' % company_id
    )
    records = companyCursor.fetchmany(1)
    if len(records) == 0:
        app.config['MY_MESSAGE']="The requested company was not found!"
        return redirect(url_for('not_found'))
    categoryCursors = db.execute( 'select category_type from category where category_id="%s"' % records[0]['category_id'])
    category = categoryCursors.fetchall()
    reviewsCursor = db.execute(
        'select user, review from reviews where company_id="%s" order by id desc'
        % company_id
    )
    reviews = reviewsCursor.fetchall()
    return render_template('details.html', reviews=reviews, company=records[0], category=category[0]['category_type'])


@app.route('/add/company', methods=['GET', 'POST'])
def add_company():
    db = get_db()
    submitted_data = request;
    if request.method == 'POST':
        submitted_data = request
        a = request.form['company_name']
        if(a == ""):
            flash("Please add a name for your company!")
            return render_template('add_company.html', data=submitted_data)
        e = request.form['company_adress']
        if(e == ""):
            flash("Please add an adress for your company!")
            return render_template('add_company.html', data=submitted_data)
        b = request.form['company_description']
        if(b == ""):
            flash("Please add a short description for your company!")
            return render_template('add_company.html', data=submitted_data)
        if request.form.get('select-category-list') == None:
            flash('Please select a category for your company!')
            return render_template('add_company.html', data=submitted_data)
        addCursor = db.execute("select category_id from category where \
            category_type='%s'" % str(request.form.get('select-category-list')))
        cat_id = addCursor.fetchall()[0]
        c = request.form['company_details']
        if(c == ""):
            flash("Please add a few details about your company!")
            return render_template('add_company.html', data=submitted_data)
        d = str(int(cat_id[0]))
        file = request.files['company_logo']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            os.rename(UPLOAD_FOLDER+filename, UPLOAD_FOLDER+a+".jpg")
        else:
            flash("No logo added for your company.You can do that later!")
            filename = "default"
        db.execute("insert into companies (company_name, \
            company_description , company_details, company_rating, \
            company_logo, company_adress, category_id) values \
            (?, ?, ?, ?, ?, ?, ?)", (a, b, c, 0, filename+".jpg", e, d)
            )
        db.commit()
        flash('Congratulations on adding your company, '+a+' to our website!Check out your profile below.')
        addCursor = db.execute("select MAX(company_id) from companies")
        cat_id = addCursor.fetchall()[0]
        return redirect(url_for('details', company_id=cat_id[0]))
    return render_template('add_company.html', data=request)
