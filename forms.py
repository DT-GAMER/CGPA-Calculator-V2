from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), 
                                                     DataRequired(), 
                                                     EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    semester = IntegerField('Semester', validators=[DataRequired(), NumberRange(min=1, max=10)])
    academic_mode = SelectField('Academic Mode', validators=[DataRequired()], choices=[('UTME', 'UTME'), ('DE', 'DE')])
    level = IntegerField('Level', validators=[DataRequired(), NumberRange(min=100, max=500)])
    previous_cgpa = StringField('Previous CGPA', validators=[DataRequired(), Length(max=4)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class AddCourseForm(FlaskForm):
    course_code = StringField('Course Code', validators=[DataRequired(), Length(max=10)])
    course_title = StringField('Course Title', validators=[DataRequired(), Length(max=100)])
    course_unit = IntegerField('Course Unit', validators=[DataRequired(), NumberRange(min=1, max=10)])
    grade = SelectField('Grade', validators=[DataRequired()], choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')])
    submit = SubmitField('Add Course')


class EditCourseForm(FlaskForm):
    course_code = StringField('Course Code', validators=[DataRequired(), Length(max=10)])
    course_title = StringField('Course Title', validators=[DataRequired(), Length(max=100)])
    course_unit = IntegerField('Course Unit', validators=[DataRequired(), NumberRange(min=1, max=10)])
    grade = SelectField('Grade', validators=[DataRequired()], choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')])
    submit = SubmitField('Save Changes')
    delete = SubmitField('Delete Course')￼Enter
