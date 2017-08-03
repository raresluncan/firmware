import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app=Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'firmware.db'),
    SECRET_KEY = 'such secret much wow so key no guess muh'
))


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
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
    return render_template('404.html', error_message="Resource not found!")


@app.route('/details/<company_id>')
def details(company_id):
    db = get_db()
    companyCursor = db.execute(
        'select * from companies where company_id="%s"' % company_id
    )
    records = companyCursor.fetchmany(1)
    if len(records) == 0:
        return redirect(url_for('not_found'))

    reviewsCursor = db.execute(
        'select user, review from reviews where company_id="%s" order by id desc'
        % company_id
    )
    reviews = reviewsCursor.fetchall()
    return render_template('details.html', reviews=reviews, company=records[0])
