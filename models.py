from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    academic_mode = db.Column(db.String(10), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    previous_cgpa = db.Column(db.Float, nullable=False)
    courses = db.relationship('Course', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(10), nullable=False)
    course_title = db.Column(db.String(100), nullable=False)
    course_unit = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Course('{self.course_code}', '{self.course_title}', '{self.course_unit}', '{self.grade}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))￼Enter
