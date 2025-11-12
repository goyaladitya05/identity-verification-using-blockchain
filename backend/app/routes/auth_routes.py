from flask import Blueprint, request, jsonify
from app.models import User
from app.utils import AuthUtil, EncryptionUtil, HashUtil
from bson.objectid import ObjectId

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'wallet_address', 'full_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        email = data['email']
        password = data['password']
        wallet_address = data['wallet_address']
        full_name = data['full_name']
        
        # Check if user already exists
        if User.get_user_by_email(email):
            return jsonify({'error': 'User with this email already exists'}), 409
        
        if User.get_user_by_wallet(wallet_address):
            return jsonify({'error': 'User with this wallet address already exists'}), 409
        
        # Hash password
        password_hash = AuthUtil.hash_password(password)
        
        # Create user
        user_id = User.create_user(email, wallet_address, full_name, password_hash)
        
        # Generate JWT token
        token = AuthUtil.generate_jwt_token(user_id, email, wallet_address)
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': str(user_id),
            'token': token,
            'user': {
                'email': email,
                'full_name': full_name,
                'wallet_address': wallet_address
            }
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Missing email or password'}), 400
        
        email = data['email']
        password = data['password']
        
        # Get user
        user = User.get_user_by_email(email)
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not AuthUtil.verify_password(password, user['password_hash']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate JWT token
        token = AuthUtil.generate_jwt_token(user['_id'], email, user['wallet_address'])
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'user_id': str(user['_id']),
                'email': user['email'],
                'full_name': user['full_name'],
                'wallet_address': user['wallet_address'],
                'is_verified': user.get('is_verified', False)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify JWT token"""
    try:
        token = AuthUtil.extract_token_from_request(request)
        
        if not token:
            return jsonify({'error': 'Missing token'}), 400
        
        payload = AuthUtil.verify_jwt_token(token)
        
        return jsonify({
            'message': 'Token is valid',
            'payload': payload
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 401
