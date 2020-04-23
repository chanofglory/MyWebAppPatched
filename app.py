
from flask import Flask, render_template, request, session, redirect
import os
from tabledef import User, Course, Order, Comment
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///tutorial.db', echo=True)
app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect('/profile')


@app.route('/login', methods=['POST'])
def do_login():
    post_username = str(request.form['username'])
    post_password = str(request.form['password'])
    s = sessionmaker(bind=engine)()
    query = s.query(User).filter(User.username.in_([post_username]), User.password.in_([post_password]))
    result = query.first()
    if result:
        session['logged_in'] = True
        session['cur_user_id'] = result.id
        return redirect('/profile')
    else:
        return 'wrong password!<br><a href="/">Back</a>'


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route("/buycourse", methods=['POST'])
def buycourse():
    s = sessionmaker(bind=engine)()
    cur_user = s.query(User).filter(User.id == session['cur_user_id']).first()
    if cur_user.balance < int(request.form['price']):
        return 'Sorry, you have no money!<br><a href="/profile">Back</a>'
    cur_user.balance -= int(request.form['price'])
    course = s.query(Course).filter(Course.id == request.form['courseid']).first()
    order = Order()
    order.course = course
    order.user = cur_user
    s.add(order)
    s.commit()
    return 'Nice buy!<br><a href="/profile">Back</a>'


# show on search in my courses
@app.route("/mycourses", methods=['POST'])
def my_courses():
    stmt = text("SELECT name, id FROM courses WHERE id IN (SELECT course_id FROM orders WHERE user_id = "
                + str(session['cur_user_id']) + ") AND name like '%" + request.form['searchString'] + "%'")
    s = sessionmaker(bind=engine)()
    results = s.query(Course).from_statement(stmt).all()
    return render_template('mycourses.html', results=results)


@app.route("/profile")
def profile_page():
    if not session['logged_in']:
        return home()
    s = sessionmaker(bind=engine)()
    cur_user = s.query(User).filter(User.id == session['cur_user_id']).first()
    courses = s.query(Course).filter(Course.id.notin_(s.query(Order.course_id).filter(Order.user_id == cur_user.id))).all()
    return render_template('profile.html', username=cur_user.username,
                           balance=cur_user.balance, courses=courses)


@app.route("/c/<cid>")
def course_page(cid):
    if not session['logged_in']:
        return home()
    s = sessionmaker(bind=engine)()
    course = s.query(Course).filter(Course.id == cid).first()
    comments = s.query(Comment).filter(Comment.course_id == cid).all()
    return render_template('course.html', course=course, comments=comments)


@app.route("/addcomment", methods=['POST'])
def add_comment():
    course_id = request.form['courseid']
    if not request.form['replytext']:
        return 'Please enter some text!<br><a href="/c/' + course_id + '">Back</a>'
    s = sessionmaker(bind=engine)()
    cur_user = s.query(User).filter(User.id == session['cur_user_id']).first()
    course = s.query(Course).filter(Course.id == course_id).first()
    cmnt = Comment(cur_user, course, request.form['replytext'])
    s.add(cmnt)
    s.commit()
    return 'Comment added!<br><a href="/c/' + course_id + '">Back</a>'


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=4000)
