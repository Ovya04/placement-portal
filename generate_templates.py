import os
from pathlib import Path

# Define all templates with their content
templates = {
    'app/templates/layout.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Placement Portal{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
    <style>
        body { background-color: #ecf0f1; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar { background: linear-gradient(135deg, #2c3e50, #3498db); box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .navbar-brand { font-weight: bold; font-size: 1.5rem; }
        .card { border: none; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; }
        .dashboard-card { padding: 20px; margin: 10px 0; border-left: 4px solid #3498db; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">📋 Placement Portal</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    {% if current_user.is_authenticated %}
                        {% if current_user.username is defined %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.dashboard') }}">Dashboard</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.manage_companies') }}">Companies</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.manage_students') }}">Students</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.manage_drives') }}">Drives</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.view_applications') }}">Applications</a></li>
                        {% elif current_user.company_name is defined %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('company.dashboard') }}">Dashboard</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('company.create_drive') }}">Create Drive</a></li>
                        {% elif current_user.student_id is defined %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('student.dashboard') }}">Dashboard</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('student.view_drives') }}">View Drives</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('student.view_applications') }}">Applications</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('student.profile') }}">Profile</a></li>
                        {% endif %}
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.logout') }}">Logout</a></li>
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.admin_login') }}">Admin Login</a></li>
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.company_register') }}">Company Register</a></li>
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.student_register') }}">Student Register</a></li>
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.login') }}">Login</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    <div class="container mt-3">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>
    <main class="container my-4">
        {% block content %}{% endblock %}
    </main>
    <footer class="bg-dark text-white text-center py-4 mt-5">
        <p>&copy; 2026 Placement Portal</p>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>''',

    'app/templates/auth/admin_login.html': '''{% extends "layout.html" %}
{% block title %}Admin Login{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-5">
        <div class="card mt-5">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0">🔐 Admin Login</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.username.label }}
                        {{ form.username(class="form-control", placeholder="Username") }}
                        {% if form.username.errors %}<small class="text-danger">{{ form.username.errors[0] }}</small>{% endif %}
                    </div>
                    <div class="mb-3">
                        {{ form.password.label }}
                        {{ form.password(class="form-control", placeholder="Password") }}
                        {% if form.password.errors %}<small class="text-danger">{{ form.password.errors[0] }}</small>{% endif %}
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
                <hr>
                <div class="alert alert-info mb-0"><small><strong>Demo:</strong> admin / admin123</small></div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'app/templates/auth/company_register.html': '''{% extends "layout.html" %}
{% block title %}Company Registration{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-7">
        <div class="card mt-3">
            <div class="card-header bg-success text-white">
                <h4 class="mb-0">🏢 Company Registration</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.company_name.label }}
                        {{ form.company_name(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.email.label }}
                        {{ form.email(class="form-control") }}
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            {{ form.password.label }}
                            {{ form.password(class="form-control") }}
                        </div>
                        <div class="col-md-6 mb-3">
                            {{ form.confirm_password.label }}
                            {{ form.confirm_password(class="form-control") }}
                        </div>
                    </div>
                    <div class="mb-3">
                        {{ form.hr_contact.label }}
                        {{ form.hr_contact(class="form-control") }}
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            {{ form.hr_phone.label }}
                            {{ form.hr_phone(class="form-control") }}
                        </div>
                        <div class="col-md-6 mb-3">
                            {{ form.website.label }}
                            {{ form.website(class="form-control") }}
                        </div>
                    </div>
                    <div class="mb-3">
                        {{ form.company_description.label }}
                        {{ form.company_description(class="form-control", rows="4") }}
                    </div>
                    <button type="submit" class="btn btn-success w-100">Register</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'app/templates/auth/student_register.html': '''{% extends "layout.html" %}
{% block title %}Student Registration{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-7">
        <div class="card mt-3">
            <div class="card-header bg-info text-white">
                <h4 class="mb-0">👨‍🎓 Student Registration</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            {{ form.student_id.label }}
                            {{ form.student_id(class="form-control") }}
                        </div>
                        <div class="col-md-6 mb-3">
                            {{ form.name.label }}
                            {{ form.name(class="form-control") }}
                        </div>
                    </div>
                    <div class="mb-3">
                        {{ form.email.label }}
                        {{ form.email(class="form-control") }}
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            {{ form.password.label }}
                            {{ form.password(class="form-control") }}
                        </div>
                        <div class="col-md-6 mb-3">
                            {{ form.confirm_password.label }}
                            {{ form.confirm_password(class="form-control") }}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            {{ form.phone.label }}
                            {{ form.phone(class="form-control") }}
                        </div>
                        <div class="col-md-6 mb-3">
                            {{ form.cgpa.label }}
                            {{ form.cgpa(class="form-control") }}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            {{ form.branch.label }}
                            {{ form.branch(class="form-control") }}
                        </div>
                        <div class="col-md-6 mb-3">
                            {{ form.year.label }}
                            {{ form.year(class="form-control") }}
                        </div>
                    </div>
                    <button type="submit" class="btn btn-info w-100">Register</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'app/templates/auth/login.html': '''{% extends "layout.html" %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-5">
        <div class="card mt-5">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0">🔐 Login</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.email.label }}
                        {{ form.email(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.password.label }}
                        {{ form.password(class="form-control") }}
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
                <hr>
                <p class="text-center">
                    <a href="{{ url_for('auth.company_register') }}" class="btn btn-sm btn-outline-success">Company Register</a><br><br>
                    <a href="{{ url_for('auth.student_register') }}" class="btn btn-sm btn-outline-info">Student Register</a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'app/templates/admin/dashboard.html': '''{% extends "layout.html" %}
{% block title %}Admin Dashboard{% endblock %}
{% block content %}
<h2 class="mb-4">📊 Admin Dashboard</h2>
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card dashboard-card bg-light">
            <h5>Total Students</h5>
            <h3 class="text-primary">{{ stats.total_students }}</h3>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card dashboard-card bg-light">
            <h5>Total Companies</h5>
            <h3 class="text-success">{{ stats.total_companies }}</h3>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card dashboard-card bg-light">
            <h5>Placement Drives</h5>
            <h3 class="text-info">{{ stats.total_drives }}</h3>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card dashboard-card bg-light">
            <h5>Applications</h5>
            <h3 class="text-warning">{{ stats.total_applications }}</h3>
        </div>
    </div>
</div>
<div class="row mt-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-danger text-white">
                <h5>⚠️ Pending Companies</h5>
            </div>
            <div class="card-body">
                <h3>{{ stats.pending_companies }}</h3>
                <a href="{{ url_for('admin.manage_companies') }}" class="btn btn-sm btn-primary">Review</a>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-danger text-white">
                <h5>⚠️ Pending Drives</h5>
            </div>
            <div class="card-body">
                <h3>{{ stats.pending_drives }}</h3>
                <a href="{{ url_for('admin.manage_drives') }}" class="btn btn-sm btn-primary">Review</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'app/templates/admin/companies.html': '''{% extends "layout.html" %}
{% block title %}Manage Companies{% endblock %}
{% block content %}
<h2 class="mb-4">🏢 Manage Companies</h2>
<div class="card">
    <table class="table table-striped mb-0">
        <thead class="table-dark">
            <tr>
                <th>Company Name</th>
                <th>Email</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for company in companies.items %}
            <tr>
                <td><strong>{{ company.company_name }}</strong></td>
                <td>{{ company.email }}</td>
                <td>
                    {% if company.approval_status == 'Pending' %}
                        <span class="badge bg-warning">Pending</span>
                    {% elif company.approval_status == 'Approved' %}
                        <span class="badge bg-success">Approved</span>
                    {% else %}
                        <span class="badge bg-danger">Rejected</span>
                    {% endif %}
                </td>
                <td>
                    {% if company.approval_status == 'Pending' %}
                        <form method="POST" style="display:inline;">
                            <button class="btn btn-sm btn-success" formaction="{{ url_for('admin.approve_company', company_id=company.id) }}">✓</button>
                            <button class="btn btn-sm btn-danger" formaction="{{ url_for('admin.reject_company', company_id=company.id) }}">✗</button>
                        </form>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'app/templates/admin/students.html': '''{% extends "layout.html" %}
{% block title %}Manage Students{% endblock %}
{% block content %}
<h2 class="mb-4">👨‍🎓 Manage Students</h2>
<div class="card">
    <table class="table table-striped mb-0">
        <thead class="table-dark">
            <tr>
                <th>Student ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for student in students.items %}
            <tr>
                <td>{{ student.student_id }}</td>
                <td>{{ student.name }}</td>
                <td>{{ student.email }}</td>
                <td>
                    <form method="POST" style="display:inline;">
                        <button class="btn btn-sm btn-warning" formaction="{{ url_for('admin.blacklist_student', student_id=student.id) }}">Blacklist</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'app/templates/admin/drives.html': '''{% extends "layout.html" %}
{% block title %}Manage Drives{% endblock %}
{% block content %}
<h2 class="mb-4">📋 Placement Drives</h2>
<div class="card">
    <table class="table table-striped mb-0">
        <thead class="table-dark">
            <tr>
                <th>Job Title</th>
                <th>Company</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for drive in drives.items %}
            <tr>
                <td>{{ drive.job_title }}</td>
                <td>{{ drive.company.company_name }}</td>
                <td>
                    {% if drive.status == 'Pending' %}
                        <span class="badge bg-warning">Pending</span>
                    {% else %}
                        <span class="badge bg-success">{{ drive.status }}</span>
                    {% endif %}
                </td>
                <td>
                    {% if drive.status == 'Pending' %}
                        <form method="POST" style="display:inline;">
                            <button class="btn btn-sm btn-success" formaction="{{ url_for('admin.approve_drive', drive_id=drive.id) }}">✓</button>
                            <button class="btn btn-sm btn-danger" formaction="{{ url_for('admin.reject_drive', drive_id=drive.id) }}">✗</button>
                        </form>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'app/templates/admin/applications.html': '''{% extends "layout.html" %}
{% block title %}Applications{% endblock %}
{% block content %}
<h2 class="mb-4">📑 All Applications</h2>
<div class="card">
    <table class="table table-striped mb-0">
        <thead class="table-dark">
            <tr>
                <th>Student</th>
                <th>Job Title</th>
                <th>Company</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for app in applications.items %}
            <tr>
                <td>{{ app.student.name }}</td>
                <td>{{ app.drive.job_title }}</td>
                <td>{{ app.drive.company.company_name }}</td>
                <td><span class="badge bg-info">{{ app.application_status }}</span></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'app/templates/company/dashboard.html': '''{% extends "layout.html" %}
{% block title %}Company Dashboard{% endblock %}
{% block content %}
<h2 class="mb-4">Welcome, <strong>{{ company.company_name }}</strong> 🏢</h2>
{% if company.approval_status != 'Approved' %}
<div class="alert alert-warning">Status: {{ company.approval_status }} - Awaiting admin approval</div>
{% endif %}
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card dashboard-card bg-light">
            <h5>Active Drives</h5>
            <h3>{{ total_drives }}</h3>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card dashboard-card bg-light">
            <h5>Applications</h5>
            <h3>{{ total_applications }}</h3>
        </div>
    </div>
</div>
{% if company.approval_status == 'Approved' %}
<a href="{{ url_for('company.create_drive') }}" class="btn btn-success mb-3">+ Create Drive</a>
{% endif %}
<div class="card">
    <h5 class="card-header">Your Drives</h5>
    <table class="table table-striped mb-0">
        <thead>
            <tr>
                <th>Job Title</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for drive in drives %}
            <tr>
                <td>{{ drive.job_title }}</td>
                <td><span class="badge bg-info">{{ drive.status }}</span></td>
                <td>
                    <a href="{{ url_for('company.view_drive_applications', drive_id=drive.id) }}" class="btn btn-sm btn-info">Applications</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'app/templates/company/create_drive.html': '''{% extends "layout.html" %}
{% block title %}Create Drive{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card mt-4">
            <div class="card-header bg-success text-white">
                <h4>Create Placement Drive</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.job_title.label }}
                        {{ form.job_title(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.job_description.label }}
                        {{ form.job_description(class="form-control", rows="5") }}
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            {{ form.salary.label }}
                            {{ form.salary(class="form-control") }}
                        </div>
                        <div class="col-md-6 mb-3">
                            {{ form.location.label }}
                            {{ form.location(class="form-control") }}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            {{ form.job_type.label }}
                            {{ form.job_type(class="form-control") }}
                        </div>
                        <div class="col-md-6 mb-3">
                            {{ form.total_positions.label }}
                            {{ form.total_positions(class="form-control") }}
                        </div>
                    </div>
                    <div class="mb-3">
                        {{ form.application_deadline.label }}
                        {{ form.application_deadline(class="form-control") }}
                    </div>
                    <button type="submit" class="btn btn-success w-100">Create</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'app/templates/company/edit_drive.html': '''{% extends "layout.html" %}
{% block title %}Edit Drive{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card mt-4">
            <div class="card-header bg-primary text-white">
                <h4>Edit Placement Drive</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.job_title.label }}
                        {{ form.job_title(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.job_description.label }}
                        {{ form.job_description(class="form-control", rows="5") }}
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            {{ form.salary.label }}
                            {{ form.salary(class="form-control") }}
                        </div>
                        <div class="col-md-6 mb-3">
                            {{ form.location.label }}
                            {{ form.location(class="form-control") }}
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Update</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'app/templates/company/drive_applications.html': '''{% extends "layout.html" %}
{% block title %}Applications{% endblock %}
{% block content %}
<h2 class="mb-4">Applications for {{ drive.job_title }}</h2>
<div class="card">
    <table class="table table-striped mb-0">
        <thead class="table-dark">
            <tr>
                <th>Student</th>
                <th>Email</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for app in applications.items %}
            <tr>
                <td>{{ app.student.name }}</td>
                <td>{{ app.student.email }}</td>
                <td><span class="badge bg-info">{{ app.application_status }}</span></td>
                <td>
                    <form method="POST" style="display:inline;" action="{{ url_for('company.update_app_status', app_id=app.id) }}">
                        <select name="status" class="form-select form-select-sm d-inline-block w-auto">
                            <option value="Applied" {% if app.application_status == 'Applied' %}selected{% endif %}>Applied</option>
                            <option value="Shortlisted" {% if app.application_status == 'Shortlisted' %}selected{% endif %}>Shortlisted</option>
                            <option value="Selected" {% if app.application_status == 'Selected' %}selected{% endif %}>Selected</option>
                            <option value="Rejected" {% if app.application_status == 'Rejected' %}selected{% endif %}>Rejected</option>
                        </select>
                        <button type="submit" class="btn btn-sm btn-primary">Update</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'app/templates/student/dashboard.html': '''{% extends "layout.html" %}
{% block title %}Student Dashboard{% endblock %}
{% block content %}
<h2 class="mb-4">Welcome, <strong>{{ student.name }}</strong> 👨‍🎓</h2>
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card dashboard-card bg-light">
            <h5>Available Drives</h5>
            <h3>{{ available_drives }}</h3>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card dashboard-card bg-light">
            <h5>My Applications</h5>
            <h3>{{ my_applications }}</h3>
        </div>
    </div>
</div>
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <h5 class="card-header">Recent Applications</h5>
            <table class="table table-sm mb-0">
                <thead>
                    <tr>
                        <th>Job</th>
                        <th>Company</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for app in recent_apps %}
                    <tr>
                        <td>{{ app.drive.job_title }}</td>
                        <td>{{ app.drive.company.company_name }}</td>
                        <td><span class="badge bg-info">{{ app.application_status }}</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <h5 class="card-header">Quick Links</h5>
            <div class="card-body d-grid gap-2">
                <a href="{{ url_for('student.view_drives') }}" class="btn btn-primary">Browse Drives</a>
                <a href="{{ url_for('student.view_applications') }}" class="btn btn-success">Applications</a>
                <a href="{{ url_for('student.history') }}" class="btn btn-warning">History</a>
                <a href="{{ url_for('student.profile') }}" class="btn btn-secondary">Profile</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'app/templates/student/view_drives.html': '''{% extends "layout.html" %}
{% block title %}View Drives{% endblock %}
{% block content %}
<h2 class="mb-4">📋 Approved Placement Drives</h2>
{% for drive in drives.items %}
<div class="card mb-3">
    <div class="card-body">
        <div class="row">
            <div class="col-md-8">
                <h5>{{ drive.job_title }}</h5>
                <p class="text-muted">{{ drive.company.company_name }}</p>
                <p>{{ drive.job_description[:150] }}...</p>
                <small>💰 {{ drive.salary or 'Not Disclosed' }} | 📍 {{ drive.location or 'TBD' }}</small>
            </div>
            <div class="col-md-4 text-end">
                {% if drive.id in applied_drives %}
                <span class="badge bg-success">✓ Applied</span>
                {% else %}
                <form method="POST" action="{{ url_for('student.apply_for_drive', drive_id=drive.id) }}">
                    <button type="submit" class="btn btn-primary">Apply</button>
                </form>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endfor %}
{% endblock %}''',

    'app/templates/student/applications.html': '''{% extends "layout.html" %}
{% block title %}My Applications{% endblock %}
{% block content %}
<h2 class="mb-4">My Applications</h2>
<div class="card">
    <table class="table table-striped mb-0">
        <thead class="table-dark">
            <tr>
                <th>Job Title</th>
                <th>Company</th>
                <th>Status</th>
                <th>Applied On</th>
            </tr>
        </thead>
        <tbody>
            {% for app in applications.items %}
            <tr>
                <td>{{ app.drive.job_title }}</td>
                <td>{{ app.drive.company.company_name }}</td>
                <td><span class="badge bg-info">{{ app.application_status }}</span></td>
                <td>{{ app.application_date.strftime('%Y-%m-%d') }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'app/templates/student/history.html': '''{% extends "layout.html" %}
{% block title %}History{% endblock %}
{% block content %}
<h2 class="mb-4">🏆 Placement History</h2>
<div class="row">
    {% for app in history %}
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-body">
                <h5>{{ app.drive.job_title }}</h5>
                <p class="text-muted">{{ app.drive.company.company_name }}</p>
                <p><span class="badge bg-{{ 'success' if app.application_status == 'Selected' else 'danger' if app.application_status == 'Rejected' else 'warning' }}">{{ app.application_status }}</span></p>
                <small>{{ app.application_date.strftime('%Y-%m-%d') }}</small>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}''',

    'app/templates/student/profile.html': '''{% extends "layout.html" %}
{% block title %}My Profile{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card mt-4">
            <div class="card-header bg-primary text-white">
                <h4>My Profile</h4>
            </div>
            <div class="card-body">
                <form method="POST" enctype="multipart/form-data">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        <strong>Student ID:</strong> {{ student.student_id }}
                    </div>
                    <div class="mb-3">
                        {{ form.name.label }}
                        {{ form.name(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        <strong>Email:</strong> {{ student.email }}
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            {{ form.phone.label }}
                            {{ form.phone(class="form-control") }}
                        </div>
                        <div class="col-md-6 mb-3">
                            {{ form.cgpa.label }}
                            {{ form.cgpa(class="form-control") }}
                        </div>
                    </div>
                    <div class="mb-3">
                        {{ form.branch.label }}
                        {{ form.branch(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.resume.label }}
                        {{ form.resume(class="form-control") }}
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Update Profile</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'app/templates/student/application_detail.html': '''{% extends "layout.html" %}
{% block title %}Application Details{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card mt-4">
            <div class="card-header bg-info text-white">
                <h4>Application Details</h4>
            </div>
            <div class="card-body">
                <h5>{{ application.drive.job_title }}</h5>
                <p><strong>Company:</strong> {{ application.drive.company.company_name }}</p>
                <p><strong>Status:</strong> <span class="badge bg-info">{{ application.application_status }}</span></p>
                <p><strong>Applied On:</strong> {{ application.application_date.strftime('%Y-%m-%d %H:%M') }}</p>
                <a href="{{ url_for('student.view_applications') }}" class="btn btn-secondary">Back</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
}

# Create directories and files
for path, content in templates.items():
    # Create directory if it doesn't exist
    dir_path = os.path.dirname(path)
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Write file
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Created: {path}")

print("\n✅ All templates generated successfully!")