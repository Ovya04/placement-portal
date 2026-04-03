from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, IntegerField, DateField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from app.models import Company, Student

# ============= AUTH FORMS =============
class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired()])

class CompanyRegistrationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=3)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    hr_contact = StringField('HR Contact Name', validators=[DataRequired()])
    hr_phone = StringField('HR Phone', validators=[Optional()])
    website = StringField('Website', validators=[Optional()])
    company_description = TextAreaField('Company Description', validators=[Optional()])
    
    def validate_email(self, field):
        if Company.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

class StudentRegistrationForm(FlaskForm):
    student_id = StringField('Student ID / Roll Number', validators=[DataRequired()])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=3)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone Number', validators=[Optional()])
    cgpa = StringField('CGPA', validators=[Optional()])
    branch = StringField('Branch/Department', validators=[Optional()])
    year = SelectField('Year', choices=[('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year')])
    
    def validate_email(self, field):
        if Student.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
    
    def validate_student_id(self, field):
        if Student.query.filter_by(student_id=field.data).first():
            raise ValidationError('Student ID already exists')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

# ============= COMPANY FORMS =============
class PlacementDriveForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])
    eligibility_criteria = TextAreaField('Eligibility Criteria', validators=[Optional()])
    salary = StringField('Salary Range', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    job_type = SelectField('Job Type', choices=[('Full-time', 'Full-time'), ('Internship', 'Internship'), ('Contract', 'Contract')])
    total_positions = IntegerField('Total Positions', validators=[DataRequired()])
    application_deadline = DateField('Application Deadline', validators=[DataRequired()])

# ============= STUDENT FORMS =============
class StudentProfileUpdateForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=3)])
    phone = StringField('Phone Number', validators=[Optional()])
    cgpa = StringField('CGPA', validators=[Optional()])
    branch = StringField('Branch/Department', validators=[Optional()])
    resume = FileField('Upload Resume (PDF/DOC)')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])