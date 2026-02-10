#!/usr/bin/env python3
"""
Database Setup Script for Flask Auth App
Creates the database, users table, and sessions table if they don't exist
"""

import pymysql

# Docker configuration defaults
DB_CONFIG = {
    "host": "mysql",
    "port": 3306,
    "user": "webd",
    "password": "Web123",
    # "database": "flask_auth"  # Optional: Add if you want to specify default database
}

def setup_database():
    """Create database, users table, and sessions table"""
    connection = None
    
    try:
        # Connect to MySQL server (without database)
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS webD")
        print("✓ Database 'webD' created or already exists")
        
        # Select the database
        cursor.execute("USE webD")
        
        # Create users table
        create_users_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_users_table_sql)
        print("✓ Users table 'users' created or already exists")
        
        # Create sessions table for Flask-Session (with id column for SQLAlchemy)
        create_sessions_table_sql = """
        CREATE TABLE IF NOT EXISTS sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(256) NOT NULL,
            data BLOB NOT NULL,
            expiry TIMESTAMP NOT NULL
        )
        """
        cursor.execute(create_sessions_table_sql)
        print("✓ Sessions table 'sessions' created or already exists")
        
        # Create customers table
        create_customers_table_sql = """
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            phone VARCHAR(50),
            company VARCHAR(255),
            address TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
        """
        cursor.execute(create_customers_table_sql)
        print("✓ Customers table 'customers' created or already exists")
        
        # Create courses table
        create_courses_table_sql = """
        CREATE TABLE IF NOT EXISTS courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            instructor VARCHAR(255),
            duration VARCHAR(100),
            level VARCHAR(50),
            price DECIMAL(10, 2),
            start_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_courses_table_sql)
        print("✓ Courses table 'courses' created or already exists")
        
        connection.commit()
        print("\n✅ Database setup completed successfully!")
        
    except pymysql.Error as e:
        print(f"❌ Error setting up database: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    setup_database()

