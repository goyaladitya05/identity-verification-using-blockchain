from flask import Blueprint, request, jsonify
from app.models import User, Credential
from app.utils import require_auth

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('/profile', methods=['GET'])
@require_auth
def get_profile():
    """Get user profile"""
    try:
        user = User.get_user_by_id(request.user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get credential count
        credentials = Credential.get_user_credentials(request.user_id)
        
        return jsonify({
            'user_id': str(user['_id']),
            'email': user['email'],
            'full_name': user['full_name'],
            'wallet_address': user['wallet_address'],
            'is_verified': user.get('is_verified', False),
            'credential_count': len(credentials),
            'verification_count': user.get('verification_count', 0),
            'created_at': user['created_at'].isoformat(),
            'updated_at': user['updated_at'].isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/profile', methods=['PUT'])
@require_auth
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        
        user = User.get_user_by_id(request.user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Only allow updating certain fields
        update_data = {}
        if 'full_name' in data:
            update_data['full_name'] = data['full_name']
        
        # Update user
        if update_data:
            User.update_user(request.user_id, update_data)
        
        updated_user = User.get_user_by_id(request.user_id)
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'user_id': str(updated_user['_id']),
                'email': updated_user['email'],
                'full_name': updated_user['full_name'],
                'wallet_address': updated_user['wallet_address'],
                'is_verified': updated_user.get('is_verified', False)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/verify/<user_id>', methods=['POST'])
def verify_user(user_id):
    """Verify a user (admin operation)"""
    try:
        # In production, this should require admin privileges
        user = User.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        User.mark_verified(user_id)
        
        return jsonify({
            'message': 'User verified successfully',
            'user_id': user_id
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/change-password', methods=['POST'])
@require_auth
def change_password():
    """Allow authenticated user to change their password"""
    try:
        data = request.get_json()
        if not data or 'old_password' not in data or 'new_password' not in data:
            return jsonify({'error': 'Missing old_password or new_password'}), 400

        old_password = data['old_password']
        new_password = data['new_password']

        user = User.get_user_by_id(request.user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Verify old password
        from app.utils.auth import AuthUtil
        if not AuthUtil.verify_password(old_password, user['password_hash']):
            return jsonify({'error': 'Old password is incorrect'}), 401

        # Hash new password and update
        new_hash = AuthUtil.hash_password(new_password)
        User.update_user(request.user_id, {'password_hash': new_hash})

        return jsonify({'message': 'Password changed successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
