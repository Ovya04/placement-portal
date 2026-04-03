from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func
from app import db
from app.models import Admin, Company, Student, PlacementDrive, Application

bp = Blueprint('admin', __name__, url_prefix='/admin')

# ============= PROTECTION DECORATOR =============
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'user_type') or current_user.user_type != 'admin':
            flash('Admin access required!', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# ============= ADMIN DASHBOARD =============
@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()
    pending_companies = Company.query.filter_by(approval_status='Pending').count()
    pending_drives = PlacementDrive.query.filter_by(status='Pending').count()
    
    stats = {
        'total_students': total_students,
        'total_companies': total_companies,
        'total_drives': total_drives,
        'total_applications': total_applications,
        'pending_companies': pending_companies,
        'pending_drives': pending_drives
    }
    
    return render_template('admin/dashboard.html', stats=stats)

# ============= MANAGE COMPANIES =============
@bp.route('/companies')
@login_required
@admin_required
def manage_companies():
    page = request.args.get('page', 1, type=int)
    companies = Company.query.paginate(page=page, per_page=10)
    return render_template('admin/companies.html', companies=companies)

@bp.route('/company/<int:company_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval_status = 'Approved'
    from datetime import datetime
    company.approved_at = datetime.utcnow()
    db.session.commit()
    flash(f'{company.company_name} approved!', 'success')
    return redirect(url_for('admin.manage_companies'))

@bp.route('/company/<int:company_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval_status = 'Rejected'
    db.session.commit()
    flash(f'{company.company_name} rejected!', 'warning')
    return redirect(url_for('admin.manage_companies'))

@bp.route('/company/<int:company_id>/blacklist', methods=['POST'])
@login_required
@admin_required
def blacklist_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.blacklist_status = not company.blacklist_status
    db.session.commit()
    status = 'blacklisted' if company.blacklist_status else 'removed from blacklist'
    flash(f'{company.company_name} {status}!', 'info')
    return redirect(url_for('admin.manage_companies'))

# ============= MANAGE STUDENTS =============
@bp.route('/students')
@login_required
@admin_required
def manage_students():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    
    if search_query:
        students = Student.query.filter(
            (Student.name.ilike(f'%{search_query}%')) |
            (Student.student_id.ilike(f'%{search_query}%')) |
            (Student.email.ilike(f'%{search_query}%'))
        ).paginate(page=page, per_page=10)
    else:
        students = Student.query.paginate(page=page, per_page=10)
    
    return render_template('admin/students.html', students=students, search_query=search_query)

@bp.route('/student/<int:student_id>/blacklist', methods=['POST'])
@login_required
@admin_required
def blacklist_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.blacklist_status = not student.blacklist_status
    db.session.commit()
    status = 'blacklisted' if student.blacklist_status else 'removed from blacklist'
    flash(f'{student.name} {status}!', 'info')
    return redirect(url_for('admin.manage_students'))

# ============= MANAGE PLACEMENT DRIVES =============
@bp.route('/drives')
@login_required
@admin_required
def manage_drives():
    page = request.args.get('page', 1, type=int)
    drives = PlacementDrive.query.paginate(page=page, per_page=10)
    return render_template('admin/drives.html', drives=drives)

@bp.route('/drive/<int:drive_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'Approved'
    from datetime import datetime
    drive.approved_at = datetime.utcnow()
    db.session.commit()
    flash(f'Drive "{drive.job_title}" approved!', 'success')
    return redirect(url_for('admin.manage_drives'))

@bp.route('/drive/<int:drive_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'Rejected'
    db.session.commit()
    flash(f'Drive "{drive.job_title}" rejected!', 'warning')
    return redirect(url_for('admin.manage_drives'))

# ============= VIEW APPLICATIONS =============
@bp.route('/applications')
@login_required
@admin_required
def view_applications():
    page = request.args.get('page', 1, type=int)
    applications = Application.query.paginate(page=page, per_page=10)
    return render_template('admin/applications.html', applications=applications)