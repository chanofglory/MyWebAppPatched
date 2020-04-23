# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///tutorial.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user1 = User("admin", "password", 1000000)
session.add(user1)

user2 = User("python", "1")
session.add(user2)

user3 = User("hacker", "lol")
session.add(user3)

course1 = Course('Курс Python', 1000, 'питоновские курсы')
session.add(course1)

course2 = Course('Курс по разработке вебприложений', 1100, 'Всё что надо для разработки')
session.add(course2)

course3 = Course('Курс для успешной жизни', 20000, 'Купи и стань успешным!')
session.add(course3)

course4 = Course('Еще курс', 20000, 'Купи и стань успешным!')
session.add(course4)

course5 = Course('Больше курсов', 20000, 'Купи и стань успешным!')
session.add(course5)

# commit the record the database
session.commit()

order1 = Order()
order1.course = course1
order1.user = user1
session.add(order1)
session.commit()
