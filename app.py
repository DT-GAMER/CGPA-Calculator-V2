from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_mail import Mail
from werkzeug.urls import url_parse
from datetime import datetime
from forms import RegistrationForm, LoginForm, AddCourseForm, EditCourseForm
from models import User, Course
from utils import send_verification_email, calculate_cgpa, generate_grade_remark, get_grade_trend, get_semester_courses


app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    semester=form.semester.data,
                    academic_mode=form.academic_mode.data,
                    level=form.level.data,
                    previous_cgpa=form.previous_cgpa.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_verification_email(user)
        flash('A verification email has been sent to your email address. Please verify your email address to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)


@app.route('/verify_email/<token>')
def verify_email(token):
    user = User.verify_verification_token(token)
    if user is None:
        flash('The verification link is invalid or has expired.', 'danger')
        return redirect(url_for('login'))
    user.email_verified = True
    db.session.commit()
    flash('Your email address has been verified. You can now log in.', 'success')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email address or password.', 'danger')
            return redirect(url_for('login'))
        if not user.email_verified:
            flash('Your email address has not been verified. Please check your email for a verification link.', 'warning')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    courses = current_user.courses
    semester = current_user.semester
    semester_courses = get_semester_courses(courses, semester)
    cgpa = calculate_cgpa(courses)
    grade_trend = get_grade_trend(courses)
    return render_template('dashboard.html', title='Dashboard', courses=semester_courses, cgpa=cgpa, grade_trend=grade_trend)


@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    form = AddCourseForm()
    if form.validate_on_submit():
        course = Course(course_code=form.course_code.data,
                        course_title=form.course_title.data,
                        course_unit=form.course_unit.data,
                        grade=form.grade.data,
                        user_id=current_user.id)
        db.session.add(course)
        db.session.commit()
        flash('The course has been added.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_course.html', title='Add Course', form=form)


@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.user != current_user:
        flash('You are not authorized to edit this course.', 'danger')
        return redirect(url_for('dashboard'))
    form = EditCourseForm()
    if form.validate_on_submit():
        course.course_code = form.course_code.data
        course.course_title = form.course_title.data
        course.course_unit = form.course_unit.data
        course.grade = form.grade.data
        db.session.commit()
        flash('The course has been updated.', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.course_code.data = course.course_code
        form.course_title.data = course.course_title
        form.course_unit.data = course.course_unit
        form.grade.data = course.grade
    return render_template('edit_course.html', title='Edit Course', form=form)


@app.route('/delete_course/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.user != current_user:
        flash('You are not authorized to delete this course.', 'danger')
        return redirect(url_for('dashboard'))
    db.session.delete(course)
    db.session.commit()
    flash('The course has been deleted.', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run()
