from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user, logout_user
from sqlalchemy import func
from app import db
from app.models import Student, PlacementDrive, Application
from app.forms import StudentProfileUpdateForm
from werkzeug.utils import secure_filename
import os

bp = Blueprint('student', __name__, url_prefix='/student')

# ============= PROTECTION =============
def student_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if not current_user.is_authenticated:
            flash('Please login first', 'warning')
            return redirect(url_for('auth.login'))
        
        # Check user type by querying database directly
        try:
            user = Student.query.get(current_user.id)
            if not user:
                logout_user()
                flash('❌ Student access required! Please login as a student.', 'danger')
                return redirect(url_for('auth.login'))
        except:
            logout_user()
            flash('❌ Error accessing student. Please login again.', 'danger')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============= STUDENT DASHBOARD =============
@bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    student = Student.query.get(current_user.id)
    
    if not student:
        flash('Student record not found', 'danger')
        logout_user()
        return redirect(url_for('auth.login'))
    
    available_drives = PlacementDrive.query.filter_by(status='Approved').count()
    my_applications = Application.query.filter_by(student_id=student.id).count()
    
    recent_apps = Application.query.filter_by(student_id=student.id).order_by(
        Application.application_date.desc()
    ).limit(5).all()
    
    return render_template('student/dashboard.html', student=student, 
                          available_drives=available_drives, my_applications=my_applications,
                          recent_apps=recent_apps)

# ============= VIEW ALL DRIVES =============
@bp.route('/drives')
@login_required
@student_required
def view_drives():
    page = request.args.get('page', 1, type=int)
    student = Student.query.get(current_user.id)
    
    if not student:
        logout_user()
        return redirect(url_for('auth.login'))
    
    drives = PlacementDrive.query.filter_by(status='Approved').paginate(page=page, per_page=10)
    applied_drives = {app.drive_id for app in student.applications}
    
    return render_template('student/view_drives.html', drives=drives, applied_drives=applied_drives)

# ============= APPLY FOR DRIVE =============
@bp.route('/drive/<int:drive_id>/apply', methods=['POST'])
@login_required
@student_required
def apply_for_drive(drive_id):
    student = Student.query.get(current_user.id)
    
    if not student:
        logout_user()
        return redirect(url_for('auth.login'))
    
    drive = PlacementDrive.query.get_or_404(drive_id)
    
    existing_app = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing_app:
        flash('❌ You have already applied for this drive!', 'warning')
        return redirect(url_for('student.view_drives'))
    
    application = Application(student_id=student.id, drive_id=drive_id)
    db.session.add(application)
    db.session.commit()
    
    flash(f'✓ Applied for {drive.job_title}!', 'success')
    return redirect(url_for('student.view_drives'))

# ============= VIEW APPLICATIONS =============
@bp.route('/applications')
@login_required
@student_required
def view_applications():
    student = Student.query.get(current_user.id)
    
    if not student:
        logout_user()
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    applications = Application.query.filter_by(student_id=student.id).paginate(page=page, per_page=10)
    
    return render_template('student/applications.html', applications=applications)

# ============= PLACEMENT HISTORY =============
@bp.route('/history')
@login_required
@student_required
def history():
    student = Student.query.get(current_user.id)
    
    if not student:
        logout_user()
        return redirect(url_for('auth.login'))
    
    history = Application.query.filter_by(student_id=student.id).all()
    
    return render_template('student/history.html', history=history)

# ============= UPDATE PROFILE =============
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
@student_required
def profile():
    student = Student.query.get(current_user.id)
    
    if not student:
        logout_user()
        return redirect(url_for('auth.login'))
    
    form = StudentProfileUpdateForm()
    
    if form.validate_on_submit():
        student.name = form.name.data
        student.phone = form.phone.data
        student.cgpa = form.cgpa.data if form.cgpa.data else student.cgpa
        student.branch = form.branch.data
        
        if form.resume.data:
            file = form.resume.data
            if allowed_file(file.filename):
                filename = secure_filename(f"{student.student_id}_{student.name.replace(' ', '_')}.{file.filename.rsplit('.', 1)[1].lower()}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                student.resume_filename = filename
                student.resume_path = filepath
            else:
                flash('❌ Invalid file format. Allowed: PDF, DOC, DOCX', 'danger')
                return render_template('student/profile.html', student=student, form=form)
        
        db.session.commit()
        flash('✓ Profile updated successfully!', 'success')
        return redirect(url_for('student.profile'))
    
    elif request.method == 'GET':
        form.name.data = student.name
        form.phone.data = student.phone
        form.cgpa.data = student.cgpa
        form.branch.data = student.branch
    
    return render_template('student/profile.html', student=student, form=form)

# ============= VIEW SINGLE APPLICATION =============
@bp.route('/application/<int:app_id>')
@login_required
@student_required
def view_application(app_id):
    student = Student.query.get(current_user.id)
    
    if not student:
        logout_user()
        return redirect(url_for('auth.login'))
    
    application = Application.query.get_or_404(app_id)
    
    if application.student_id != current_user.id:
        flash('❌ Unauthorized!', 'danger')
        return redirect(url_for('student.dashboard'))
    
    return render_template('student/application_detail.html', application=application)