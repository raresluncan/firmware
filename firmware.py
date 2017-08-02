import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app=Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'firmware.db'),
    SECRET_KEY='such secret much wow so key no guess muh'
))


def connect_db():
    rv=sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

    
def init_db():
    db=get_db()
    with app.open_resource('schema.sql',mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print("Firmware initialized database sucessfully!")
def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db=connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_home():
    db = get_db()
    cur = db.execute("select * from companies")
    companies = cur.fetchall()
    return render_template('index.html',companies=companies)


@app.route('/details/<company_id>')
def show_details(company_id):
    db = get_db()
    cur = db.execute("select user, review from reviews where company_id="+company_id+" order by id desc")
    reviews = cur.fetchall()
    db = get_db()
    cur = db.execute("select * from companies where company_id="+company_id)
    rows=cur.fetchall()
    return render_template('details.html', reviews=reviews, rows=rows)
