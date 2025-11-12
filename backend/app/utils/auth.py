import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
JWT_EXPIRATION = int(os.getenv("JWT_EXPIRATION", "86400"))  # 24 hours

class AuthUtil:
    """Utilities for authentication and authorization"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password, password_hash):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    @staticmethod
    def generate_jwt_token(user_id, email, wallet_address):
        """Generate JWT token"""
        payload = {
            'user_id': str(user_id),
            'email': email,
            'wallet_address': wallet_address,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return token
    
    @staticmethod
    def verify_jwt_token(token):
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
    
    @staticmethod
    def extract_token_from_request(req):
        """Extract JWT token from request headers"""
        auth_header = req.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
        return auth_header[7:]  # Remove 'Bearer ' prefix


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = AuthUtil.extract_token_from_request(request)
        if not token:
            return jsonify({'error': 'Missing authentication token'}), 401
        
        try:
            payload = AuthUtil.verify_jwt_token(token)
            request.user_id = payload['user_id']
            request.email = payload['email']
            request.wallet_address = payload['wallet_address']
        except Exception as e:
            return jsonify({'error': str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
