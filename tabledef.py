from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', back_populates='course_orders')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='user_orders')


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='user_comments')
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship('Course', back_populates='course_comments')
    text = Column(String)

    def __init__(self, author, course, text):
        self.author = author
        self.course = course
        self.text = text


class Course(Base):
    __tablename__ = "courses"
    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    desc = Column(String)
    course_orders = relationship('Order', order_by=Order.id, back_populates='course')
    course_comments = relationship('Comment', order_by=Comment.id, back_populates='course')

    def __init__(self, name, price, desc=''):
        self.name = name
        self.price = price
        self.desc = desc
        self.id = str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    balance = Column(Integer)
    user_orders = relationship('Order', order_by=Order.id, back_populates='user')
    user_comments = relationship('Comment', order_by=Comment.id, back_populates='author')

    def __init__(self, username, password, balance=1100):
        self.username = username
        self.password = password
        self.balance = balance


# create tables
Base.metadata.create_all(engine)
