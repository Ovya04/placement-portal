from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'placement-portal-secret-key-2024'
    
    # Database configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}/../database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from .routes import auth, admin, company, student
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(company.bp)
    app.register_blueprint(student.bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
        # Create default admin if doesn't exist
        from .models import Admin
        if not Admin.query.filter_by(username='admin').first():
            admin_user = Admin(
                username='admin',
                email='admin@institute.com',
                role='Admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("✓ Default Admin created: admin / admin123")
    
    return app

@login_manager.user_loader
def load_user(user_id):
    """
    Load user from database based on user_id.
    Since we have multiple user types (Admin, Company, Student),
    we need to check all tables.
    """
    from .models import Admin, Company, Student
    
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return None
    
    # Try to find in Admin table first
    user = Admin.query.get(user_id_int)
    if user:
        return user
    
    # Then try Company table
    user = Company.query.get(user_id_int)
    if user:
        return user
    
    # Finally try Student table
    user = Student.query.get(user_id_int)
    if user:
        return user
    
    return None