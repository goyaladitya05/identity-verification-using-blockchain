import os
import json
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # MongoDB
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    DB_NAME = os.getenv('DB_NAME', 'identity_verification')
    
    # JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key')
    JWT_EXPIRATION = int(os.getenv('JWT_EXPIRATION', 86400))  # 24 hours
    
    # Blockchain
    WEB3_PROVIDER_URI = os.getenv('WEB3_PROVIDER_URI', 'http://127.0.0.1:8545')
    CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '0x0000000000000000000000000000000000000000')
    PRIVATE_KEY = os.getenv('PRIVATE_KEY', '')
    GAS_LIMIT = int(os.getenv('GAS_LIMIT', 3000000))
    
    # Server
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGODB_URI = 'mongodb://localhost:27017/test_db'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


# Configuration selector
def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()
