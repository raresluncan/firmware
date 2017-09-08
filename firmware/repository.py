"""Repository - module to communicate with the database"""

from firmware.database import db_session
from firmware.models import User, Company, Category, Review
from sqlalchemy import and_


def get_companies():
    """ gets all companies from database """
    companies = db_session.query(Company)
    return companies


def get_user_id(username):
    """ gets a user id via it's unique username """
    user_id = db_session.query(User.id).filter(User.username == username)
    return user_id


def add_company(company):
    """ adds a company to the database """
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
    """ gets a category for a specific company """
    company = db_session.query(Company).filter(Company.id == company_id).one()
    category = db_session.query(Category).filter(company.category_id ==
                                                 Category.id).one()
    return category.domain


def get_categories():
    """ gets all categories from the database """
    categories = db_session.query(Category).all()
    return categories


def get_reviews(company_id):
    """ gets all reviews for a company """
    reviews = db_session.query(Review).filter(Review.company_id == company_id)\
                .order_by(Review.id.desc()).all()
    return reviews


def add_user(user):
    """ adds a new user to the database """
    db_session.add(user)
    db_session.commit()
    return user.id, user.username


def get_user(username):
    """gets a user by unique username """
    user = db_session.query(User).filter(User.username == username).one().serialize()
    return user


def check_user(username, password):
    """ checks if the user exists in the database, with the entered password """
    compatible_user = db_session.query(User).filter(and_(User.username == username,
                                                         User.password == password)).all()
    if not compatible_user:
        return 0
    return 1


def add_reviews(review):
    """ adds a review entered by a user for a company """
    db_session.add(review)
    db_session.commit()
    return None


def get_filtered_companies(category_domain):
    """ gets companies that have a specific category """
    category_id = db_session.query(Category.id).filter(Category.domain == category_domain)
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
    """ retrieves a category domain by it's id """
    category = db_session.query(Category).filter(Category.id == category_id).one()
    return category


def update_company(company, company_id):
    """ updates a company in the database """
    old_company = db_session.query(Company).get(company_id)
    company = dict(company)
    for key, value in company.items():
        setattr(old_company, key, value)
    db_session.commit()
    return company_id
