"""Repository - module to communicate with the database"""


import sqlite3
from firmware.uploaders import upload_file
from firmware import app
from flask import g
from firmware.database import db_session
from models import User, Company, Category
from sqlalchemy import and_
from sqlalchemy.orm import lazyload
import pdb


def connect_db():
    """ connects to the database """
    connection = sqlite3.connect(app.config['DATABASE'], timeout=1)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """ initializes the database """
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as firmware_schema:
        db.cursor().executescript(firmware_schema.read())
    db.commit()


def get_db():
    """ retreieves the database """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def shutdown_session(exception=None):
    pass
    # db_session.remove()


@app.teardown_appcontext
def close_db(error):
    """ closes database when application dies """
    if error is None:
        error = dict()
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_companies():
    """ gets all companies from database """
    companies = db_session.query(Company)
    return companies


def get_user_id(username):
    """ gets a user id via it's unique username """
    user_id = db_session.query(User.id).filter(User.username == username)
    return user_id


def add_company(company, company_files):
    """ adds a company to the database """
    db = get_db()
    pdb.set_trace()
    db_session.add(company)
    db_session.commit()
    return company.id


def get_company(company_id):
    """ retrieves a specific company, via it's id """
    company = db_session.query(Company).filter(Company.id == company_id).one()
    if company is None:
        return None
    return company


def get_category(company_id):
    """ gets a category from the database by it's id """
    db = get_db()
    category_query = db.execute('select type from categories where \
    id = "%s"' % get_company(company_id).category_id)
    category = category_query.fetchall()
    return category[0]['type']


def get_categories():
    """ gets all categories from the database """
    db = get_db()
    categories_query = db.execute('select * from categories')
    categories = categories_query.fetchall()
    return categories


def get_reviews(company_id):
    """ gets all reviews for a company """
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
    """ adds a new user to the database """
    u = User(user['username'],
                                       user['password'],
                                       user['email'],
                                       user.get('real_name', '-'),
                                       user['surname'],
                                       upload_file(user_files['user_avatar'],
                                                   user['username'], 'Avatars'),
                                       user['contact'],
                                       user['radio-group-privilege'],
                                       user['radio-group-gender'])
    db_session.add(u)
    return db_session.commit()

def get_user(username):
    user = db_session.query(User).filter(User.username == username).one().serialize()
    return user


def check_user(username, password):
    """ checks if the user exists in the database, with the entered password """
    compatible_user = db_session.query(User).filter(and_(User.username == username,
                                                         User.password == password)).all()
    if not compatible_user:
        return 0
    return 1


def add_reviews(company_id, user, text):
    """ adds a review entered by a user for a company """
    db = get_db()
    get_user_id_query = db.execute("select id from users where username='%s'"
                                   % user)
    user_id_row = get_user_id_query.fetchmany()
    user_id = user_id_row[0]['id']
    db.execute("insert into reviews (user_id, review, \
    company_id) values (?, ?, ?)", (user_id, text, company_id))
    db.commit()
    return None


def get_category_id(category):
    """ retrieves the if of a given category(if exists) """
    db = get_db()
    get_category_id_query = db.execute("select id from categories where \
        type = '%s'" % category)
    category_id_row = get_category_id_query.fetchmany()
    category_id = category_id_row[0]['id']
    return category_id


def get_filtered_companies(category_type):
    """ gets companies that have a specific category """
    category_id = db_session.query(Category.id).filter(Category.type == category_type)
    filtered_companies = db_session.query(Company).filter(Company.category_id == category_id)
    return filtered_companies


def get_username_by_id(user_id):
    """ retrieves a username for a given user_id """
    user = db_session.query(User).filter(User.id == user_id).one()
    return user.username


def fragment_company(company_id):
    """ fragments data of a company row into a dictionary """
    company = get_company(company_id)
    data = dict()
    data['name'] = company.name
    data['description'] = company.description
    data['details'] = company.details
    data['rating'] = company.rating
    data['logo'] = company.logo
    data['adress'] = company.adress
    data['category'] = get_category(company.id)
    data['added-by-user'] = get_username_by_id(company.added_by_id)
    return data


def get_category_by_id(category_id):
    """ retrieves a category type by it's id """
    db = get_db()
    get_category_query = db.execute("select type from categories where id='%s'"
                                    % category_id)
    get_category_row = get_category_query.fetchmany()
    category = get_category_row[0]['type']
    return category


def update_company(company, company_files, company_id):
    """ updates a company in the database """
    db = get_db()
    pdb.set_trace()
    db.execute("update companies set name = ?,description = ?,details = ?,\
        logo = ?,adress = ?,category_id = ? where id = ?", \
        (company['name'],
         company['description'],
         company['details'],
         upload_file(company_files['logo'],
                     company['name'], 'Images'),
         company['adress'],
         company.get('category'),
         company_id))
    db.commit()
    company_id_query = db.execute("select id from companies where id='%s'"
                                  % company_id)
    updated_company_id = company_id_query.fetchall()[0]
    return updated_company_id[0]
