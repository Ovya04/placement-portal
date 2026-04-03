from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ============= ADMIN MODEL =============
class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='Admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_type = 'admin'  # Add this
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

# ============= COMPANY MODEL =============
class Company(UserMixin, db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    hr_contact = db.Column(db.String(50), nullable=False)
    hr_phone = db.Column(db.String(15))
    website = db.Column(db.String(100))
    company_description = db.Column(db.Text)
    approval_status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    blacklist_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    
    user_type = 'company'  # Add this
    
    # Relationships
    placement_drives = db.relationship('PlacementDrive', backref='company', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Company {self.company_name}>'

# ============= STUDENT MODEL =============
class Student(UserMixin, db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)  # Roll number/ID
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15))
    cgpa = db.Column(db.Float)
    branch = db.Column(db.String(50))
    year = db.Column(db.String(20))
    resume_filename = db.Column(db.String(200))
    resume_path = db.Column(db.String(300))
    status = db.Column(db.String(20), default='Active')  # Active, Inactive, Blacklisted
    blacklist_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_type = 'student'  # Add this
    
    # Relationships
    applications = db.relationship('Application', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Student {self.name}>'

# ============= PLACEMENT DRIVE MODEL =============
class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility_criteria = db.Column(db.Text)
    salary = db.Column(db.String(50))
    location = db.Column(db.String(100))
    job_type = db.Column(db.String(50))  # Full-time, Internship, etc.
    application_deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Closed, Rejected
    total_positions = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    
    # Relationships
    applications = db.relationship('Application', backref='drive', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PlacementDrive {self.job_title}>'

# ============= APPLICATION MODEL =============
class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    application_status = db.Column(db.String(20), default='Applied')  # Applied, Shortlisted, Selected, Rejected
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    result_date = db.Column(db.DateTime)
    comments = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Application Student:{self.student_id} Drive:{self.drive_id}>'