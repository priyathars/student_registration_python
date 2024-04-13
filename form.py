from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, EmailField, SelectField
from wtforms.validators import DataRequired, Email
from wtforms.fields import TelField


# Creating LoginForm Class
class LoginForm(FlaskForm):
    username = StringField('Username ', validators=[DataRequired()])
    password = PasswordField('Password')
    login = SubmitField('Login')


# Creating StudentForm Class
class StudentForm(FlaskForm):
    student_name = StringField("Student Name", validators=[DataRequired()])
    dob = DateField("Date of birth", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    mobile_no = TelField("Mobile Number", [DataRequired()])
    gender = SelectField("Gender", choices=['Please select...', 'Male', 'Female'])
    course = SelectField("Course",
                         choices=['Please select...', 'Data Science', 'Software Development', 'Web Development',
                                  'Project Management', 'Artificial Intelligence'])
    submit = SubmitField("REGISTER")
