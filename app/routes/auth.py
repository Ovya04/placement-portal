from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import Admin, Company, Student
from app.forms import AdminLoginForm, CompanyRegistrationForm, StudentRegistrationForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

def clear_session_and_login(user):
    """Properly clear session and login new user"""
    logout_user()
    session.clear()
    login_user(user, remember=False)

# ============= ADMIN LOGIN =============
@bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if hasattr(current_user, 'user_type') and current_user.user_type == 'admin':
            return redirect(url_for('admin.dashboard'))
        logout_user()
    
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            clear_session_and_login(admin)
            flash(f'✓ Welcome back, {admin.username}!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('❌ Invalid admin credentials', 'danger')
    
    return render_template('auth/admin_login.html', form=form)

# ============= COMPANY REGISTRATION =============
@bp.route('/company-register', methods=['GET', 'POST'])
def company_register():
    if current_user.is_authenticated:
        if hasattr(current_user, 'user_type') and current_user.user_type == 'company':
            return redirect(url_for('company.dashboard'))
        logout_user()
    
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        existing = Company.query.filter_by(email=form.email.data).first()
        if existing:
            flash('❌ Email already registered!', 'danger')
            return render_template('auth/company_register.html', form=form)
        
        company = Company(
            company_name=form.company_name.data,
            email=form.email.data,
            hr_contact=form.hr_contact.data,
            hr_phone=form.hr_phone.data,
            website=form.website.data,
            company_description=form.company_description.data
        )
        company.set_password(form.password.data)
        
        db.session.add(company)
        db.session.commit()
        
        flash(f'✓ {form.company_name.data} registered! Awaiting admin approval.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/company_register.html', form=form)

# ============= STUDENT REGISTRATION =============
@bp.route('/student-register', methods=['GET', 'POST'])
def student_register():
    if current_user.is_authenticated:
        if hasattr(current_user, 'user_type') and current_user.user_type == 'student':
            return redirect(url_for('student.dashboard'))
        logout_user()
    
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        existing_email = Student.query.filter_by(email=form.email.data).first()
        existing_id = Student.query.filter_by(student_id=form.student_id.data).first()
        
        if existing_email:
            flash('❌ Email already registered!', 'danger')
            return render_template('auth/student_register.html', form=form)
        if existing_id:
            flash('❌ Student ID already exists!', 'danger')
            return render_template('auth/student_register.html', form=form)
        
        student = Student(
            student_id=form.student_id.data,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            cgpa=form.cgpa.data if form.cgpa.data else None,
            branch=form.branch.data,
            year=form.year.data
        )
        student.set_password(form.password.data)
        
        db.session.add(student)
        db.session.commit()
        
        flash(f'✓ {form.name.data} registered! You can now login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/student_register.html', form=form)

# ============= COMPANY/STUDENT LOGIN =============
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # If already authenticated, redirect to appropriate dashboard
    if current_user.is_authenticated:
        company = Company.query.get(current_user.id)
        if company:
            return redirect(url_for('company.dashboard'))
        
        student = Student.query.get(current_user.id)
        if student:
            return redirect(url_for('student.dashboard'))
        
        logout_user()
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        password = form.password.data
        
        # Try company first
        company = Company.query.filter_by(email=email).first()
        if company:
            if company.check_password(password):
                if company.blacklist_status:
                    flash('❌ Your account has been blacklisted.', 'danger')
                    return render_template('auth/login.html', form=form)
                elif company.approval_status != 'Approved':
                    flash('⏳ Your account is pending admin approval.', 'warning')
                    return render_template('auth/login.html', form=form)
                else:
                    logout_user()  # Clear any previous session
                    login_user(company, remember=False)
                    flash(f'✓ Welcome, {company.company_name}!', 'success')
                    return redirect(url_for('company.dashboard'))
            else:
                flash('❌ Invalid password!', 'danger')
                return render_template('auth/login.html', form=form)
        
        # Try student
        student = Student.query.filter_by(email=email).first()
        if student:
            if student.check_password(password):
                if student.blacklist_status:
                    flash('❌ Your account has been blacklisted.', 'danger')
                    return render_template('auth/login.html', form=form)
                else:
                    logout_user()  # Clear any previous session
                    login_user(student, remember=False)
                    flash(f'✓ Welcome, {student.name}!', 'success')
                    return redirect(url_for('student.dashboard'))
            else:
                flash('❌ Invalid password!', 'danger')
                return render_template('auth/login.html', form=form)
        
        flash('❌ Email not registered. Please register first.', 'danger')
    
    return render_template('auth/login.html', form=form)

# ============= LOGOUT =============
@bp.route('/logout')
def logout():
    user_name = current_user.company_name if hasattr(current_user, 'company_name') else \
                current_user.name if hasattr(current_user, 'name') else \
                current_user.username if hasattr(current_user, 'username') else 'User'
    
    logout_user()
    session.clear()
    flash(f'✓ {user_name} logged out.', 'info')
    return redirect(url_for('auth.login'))