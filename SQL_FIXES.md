# SQL Fixes - TODO List

## Issue: Flask-Session Configuration Conflict

### Problems Identified:
1. config.py had configuration conflicts between filesystem and sqlalchemy sessions
2. Flask-SQLAlchemy initialization conflict with Flask-Session
3. Sessions table schema was not compatible

### Fix Plan:
- [x] 1. Update config.py to use SESSION_TYPE = "filesystem" (simpler approach)
- [x] 2. Update app.py to remove Flask-SQLAlchemy (use raw pymysql instead)
- [x] 3. Simplify init_db() function - remove sessions table creation
- [x] 4. Test the fixes by running the application

## Summary of Changes:

### config.py:
- Reverted to `SESSION_TYPE = "filesystem"` for simpler session management
- Removed conflicting SQLAlchemy configurations

### app.py:
- Removed `from flask_sqlalchemy import SQLAlchemy` import
- Removed `db = SQLAlchemy(app)` initialization
- Simplified `init_db()` - removed sessions table creation
- Kept raw pymysql connections for database operations

## Result:
The application now uses filesystem-based sessions which is simpler and works with the existing raw pymysql connection approach. All database operations (users, customers, courses) still work correctly.

