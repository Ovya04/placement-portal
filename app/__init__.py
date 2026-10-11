from flask import Flask, url_for
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # 1. Secret Key handling (production env vs dev fallback)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'placement-portal-secret-key-2024')
    
    # 2. Database configuration (PostgreSQL for Render, SQLite for Local)
    db_url = os.environ.get('DATABASE_URL')
    
    if db_url:
        # Render internal PostgreSQL URLs start with postgres://, but SQLAlchemy requires postgresql://
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    else:
        # Local SQLite fallback
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}/../database.db'
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 3. Upload folder setup
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # 4. Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # 5. Register blueprints
    from .routes import auth, admin, company, student
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(company.bp)
    app.register_blueprint(student.bp)
    
    # 6. Auto-create database tables & initial data
    with app.app_context():
        db.create_all()
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
    
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
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