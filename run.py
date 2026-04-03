from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("🎓 PLACEMENT PORTAL APPLICATION")
    print("=" * 60)
    print("\n✓ Admin Default Credentials:")
    print("  - Username: admin")
    print("  - Password: admin123")
    print("\n✓ Access URLs:")
    print("  - Admin Login: http://localhost:5000/auth/admin-login")
    print("  - Company Register: http://localhost:5000/auth/company-register")
    print("  - Student Register: http://localhost:5000/auth/student-register")
    print("  - Login: http://localhost:5000/auth/login")
    print("\n" + "=" * 60 + "\n")
    app.run(debug=True, host='localhost', port=5000)