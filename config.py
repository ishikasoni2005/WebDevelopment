#!/usr/bin/env python3
"""
Configuration settings for Flask Auth App
"""

import os


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "123456"
    
    # Database configuration - Docker defaults
    DB_HOST = os.environ.get("DB_HOST") or "mysql"
    DB_PORT = int(os.environ.get("DB_PORT") or 3306)
    DB_USER = os.environ.get("DB_USER") or "webd"
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or "Web123"
    DB_NAME = os.environ.get("DB_NAME") or "webD"
    
    # Flask-Session configuration for server-side sessions
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = "/tmp/flask_sessions"
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
