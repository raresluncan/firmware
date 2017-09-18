"""Repository - module to communicate with the database"""

from firmware.database import db_session
from firmware.models import User, Company, Category, Review
from sqlalchemy import and_



def get_companies():
    """ gets all companies from database """
    return db_session.query(Company)


def add_company(company):
    """ adds a company to the database """
    db_session.add(company)
    db_session.commit()
    return company


def get_company(company_id):
    """ retrieves a specific company, via it's id """
    return db_session.query(Company).filter(Company.id == company_id).one()


def get_categories():
    """ gets all categories from the database """
    return db_session.query(Category).all()


def get_reviews(company_id):
    """ gets all reviews for a company """
    return db_session.query(Review).filter(Review.company_id == company_id)\
                                             .order_by(Review.id.desc()).all()


def add_user(user):
    """ adds a new user to the database """
    db_session.add(user)
    db_session.commit()
    return user


def get_user(username):
    """gets a user by unique username """
    user = db_session.query(User).filter(User.username == username).one()
    return user


def check_user(username, password):
    """ checks if the user exists in the database, with the entered password """
    user = db_session.query(User).filter(and_(User.username == username,
                                              User.password == password)).all()
    if user == []:
        return None
    return user


def add_review(review):
    """ adds a review entered by a user for a company """
    db_session.add(review)
    db_session.commit()
    return review


def get_filtered_companies(category_domain):
    """ gets companies that have a specific category """
    category_id = db_session.query(Category.id).filter(
        Category.domain == category_domain
    )
    return db_session.query(Company).filter(Company.category_id == category_id)


def get_category_by_id(category_id):
    """ retrieves a category domain by it's id """
    return db_session.query(Category).filter(Category.id == category_id).one()


def update_company(new_data, company_id):
    """ updates a company in the database """
    company = db_session.query(Company).get(company_id)
    for key, value in new_data.items():
        setattr(company, key, value)
    db_session.commit()
    return company
