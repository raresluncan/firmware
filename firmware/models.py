"""Mappers for firmware database tables"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from firmware.database import Base, engine


class User(Base):
    """defines / maps users table in database"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(21), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    name = Column(String(100))
    surname = Column(String(100))
    avatar = Column(String(100), nullable=False)
    contact = Column(String(100))
    privilege = Column(String(100), nullable=False)
    gender = Column(String(100), nullable=False)
    reviews = relationship("Review", backref='user',
                           primaryjoin="User.id == Review.user_id")
    added_company = relationship("Company", backref='added_by_user',
                                 primaryjoin="User.id==Company.added_by_id")

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.email = kwargs.get('email', None)
        self.name = kwargs.get('name', None)
        self.surname = kwargs.get('surname', None)
        self.avatar = kwargs.get('avatar', 'default.jpg')
        self.contact = kwargs.get('contact', None)
        self.privilege = kwargs.get('privilege', None)
        self.gender = kwargs.get('gender', None)

    def serialize(self):
        """returns a dictionary to store in session to remember logged user"""
        return {'id': self.id,
                'username': self.username,
                'email': self.email,
                'name': self.name,
                'surname': self.surname,
                'avatar': self.avatar,
                'contact': self.contact,
                'privilege': self.privilege,
                'gender': self.gender
               }


class Review(Base):
    """defines / maps reviews table in database"""
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(2000), nullable=False)
    company_id = Column(String(2000), ForeignKey("companies.id"),
                        nullable=False)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id', None)
        self.message = kwargs.get('message', None)
        self.company_id = kwargs.get('company_id', None)

class Company(Base):
    """defines / maps companies table in database"""
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    description = Column(String(100), nullable=False)
    details = Column(String(2001), nullable=False)
    rating = Column(Integer, nullable=False)
    logo = Column(String(36), nullable=False)
    adress = Column(String(150), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    added_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    categories = relationship("Category")
    users = relationship("User")

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.details = kwargs.get('details', None)
        self.rating = kwargs.get('rating', 0)
        self.logo = kwargs.get('logo', 'default.jpg')
        self.adress = kwargs.get('adress', None)
        self.category_id = kwargs.get('category_id', None)
        self.added_by_id = kwargs.get('added_by_id', None)

    def __iter__(self):
        yield 'name', self.name
        yield 'description', self.description
        yield 'details', self.details
        yield 'logo', self.logo
        yield 'adress', self.adress
        yield 'category_id', self.category_id

    def to_dict(self):
        """returns the data in the model object to a mutable dictionary form"""
        return {
            'name': self.name,
            'description': self.description,
            'details': self.details,
            'rating': self.rating,
            'logo': self.logo,
            'adress': self.adress,
            'category_id': self.category.id,
            'added_by_user': self.added_by_user,
        }


class Category(Base):
    """defines / maps categories table in database """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    domain = Column(String(20), unique=True, nullable=False)
    category = relationship("Company", backref='category',
                            primaryjoin="Category.id == Company.category_id")

    def __init__(self, id, domain):
        self.id = id
        self.domain = domain


Base.metadata.create_all(engine)
