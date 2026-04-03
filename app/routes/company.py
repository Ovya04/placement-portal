from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user
from sqlalchemy import func
from app import db
from app.models import Company, PlacementDrive, Application

bp = Blueprint('company', __name__, url_prefix='/company')

# ============= PROTECTION =============
def company_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if not current_user.is_authenticated:
            flash('Please login first', 'warning')
            return redirect(url_for('auth.login'))
        
        # Check user type by querying database directly
        try:
            user = Company.query.get(current_user.id)
            if not user:
                logout_user()
                flash('❌ Company access required! Please login as a company.', 'danger')
                return redirect(url_for('auth.login'))
        except:
            logout_user()
            flash('❌ Error accessing company. Please login again.', 'danger')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

# ============= COMPANY DASHBOARD =============
@bp.route('/dashboard')
@login_required
@company_required
def dashboard():
    company = Company.query.get(current_user.id)
    
    if not company:
        flash('Company record not found', 'danger')
        logout_user()
        return redirect(url_for('auth.login'))
    
    total_drives = PlacementDrive.query.filter_by(company_id=company.id).count()
    
    total_applications = db.session.query(func.count(Application.id)).join(
        PlacementDrive, Application.drive_id == PlacementDrive.id
    ).filter(PlacementDrive.company_id == company.id).scalar() or 0
    
    drives = PlacementDrive.query.filter_by(company_id=company.id).all()
    
    return render_template('company/dashboard.html', company=company, total_drives=total_drives, 
                         total_applications=total_applications, drives=drives)

# ============= CREATE PLACEMENT DRIVE =============
@bp.route('/create-drive', methods=['GET', 'POST'])
@login_required
@company_required
def create_drive():
    company = Company.query.get(current_user.id)
    
    if not company:
        flash('Company record not found', 'danger')
        logout_user()
        return redirect(url_for('auth.login'))
    
    if company.approval_status != 'Approved':
        flash('Your company must be approved by admin to create drives.', 'warning')
        return redirect(url_for('company.dashboard'))
    
    from app.forms import PlacementDriveForm
    form = PlacementDriveForm()
    
    if form.validate_on_submit():
        drive = PlacementDrive(
            company_id=company.id,
            job_title=form.job_title.data,
            job_description=form.job_description.data,
            eligibility_criteria=form.eligibility_criteria.data,
            salary=form.salary.data,
            location=form.location.data,
            job_type=form.job_type.data,
            total_positions=form.total_positions.data,
            application_deadline=form.application_deadline.data,
            status='Pending'
        )
        db.session.add(drive)
        db.session.commit()
        flash('✓ Placement drive created! Awaiting admin approval.', 'success')
        return redirect(url_for('company.dashboard'))
    
    return render_template('company/create_drive.html', form=form)

# ============= EDIT PLACEMENT DRIVE =============
@bp.route('/drive/<int:drive_id>/edit', methods=['GET', 'POST'])
@login_required
@company_required
def edit_drive(drive_id):
    company = Company.query.get(current_user.id)
    
    if not company:
        logout_user()
        return redirect(url_for('auth.login'))
    
    drive = PlacementDrive.query.get_or_404(drive_id)
    
    if drive.company_id != current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('company.dashboard'))
    
    from app.forms import PlacementDriveForm
    form = PlacementDriveForm()
    
    if form.validate_on_submit():
        drive.job_title = form.job_title.data
        drive.job_description = form.job_description.data
        drive.eligibility_criteria = form.eligibility_criteria.data
        drive.salary = form.salary.data
        drive.location = form.location.data
        drive.job_type = form.job_type.data
        drive.total_positions = form.total_positions.data
        drive.application_deadline = form.application_deadline.data
        db.session.commit()
        flash('✓ Placement drive updated!', 'success')
        return redirect(url_for('company.dashboard'))
    elif request.method == 'GET':
        form.job_title.data = drive.job_title
        form.job_description.data = drive.job_description
        form.eligibility_criteria.data = drive.eligibility_criteria
        form.salary.data = drive.salary
        form.location.data = drive.location
        form.job_type.data = drive.job_type
        form.total_positions.data = drive.total_positions
        form.application_deadline.data = drive.application_deadline
    
    return render_template('company/edit_drive.html', form=form, drive=drive)

# ============= VIEW DRIVE APPLICATIONS =============
@bp.route('/drive/<int:drive_id>/applications')
@login_required
@company_required
def view_drive_applications(drive_id):
    company = Company.query.get(current_user.id)
    
    if not company:
        logout_user()
        return redirect(url_for('auth.login'))
    
    drive = PlacementDrive.query.get_or_404(drive_id)
    
    if drive.company_id != current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('company.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    applications = Application.query.filter_by(drive_id=drive_id).paginate(page=page, per_page=10)
    
    return render_template('company/drive_applications.html', drive=drive, applications=applications)

# ============= UPDATE APPLICATION STATUS =============
@bp.route('/application/<int:app_id>/update-status', methods=['POST'])
@login_required
@company_required
def update_app_status(app_id):
    company = Company.query.get(current_user.id)
    
    if not company:
        logout_user()
        return redirect(url_for('auth.login'))
    
    application = Application.query.get_or_404(app_id)
    drive = PlacementDrive.query.get(application.drive_id)
    
    if drive.company_id != current_user.id:
        flash('Unauthorized!', 'danger')
        return redirect(url_for('company.dashboard'))
    
    new_status = request.form.get('status')
    application.application_status = new_status
    from datetime import datetime
    application.result_date = datetime.utcnow()
    db.session.commit()
    
    flash(f'✓ Application status updated to {new_status}!', 'success')
    return redirect(url_for('company.view_drive_applications', drive_id=drive.id))

# ============= DELETE DRIVE =============
@bp.route('/drive/<int:drive_id>/delete', methods=['POST'])
@login_required
@company_required
def delete_drive(drive_id):
    company = Company.query.get(current_user.id)
    
    if not company:
        logout_user()
        return redirect(url_for('auth.login'))
    
    drive = PlacementDrive.query.get_or_404(drive_id)
    
    if drive.company_id != current_user.id:
        flash('Unauthorized!', 'danger')
        return redirect(url_for('company.dashboard'))
    
    db.session.delete(drive)
    db.session.commit()
    flash('✓ Drive deleted!', 'success')
    return redirect(url_for('company.dashboard'))