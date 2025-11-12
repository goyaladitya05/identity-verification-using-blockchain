from flask import Blueprint, request, jsonify
from app.models import User, Credential
from app.utils import require_auth, EncryptionUtil, HashUtil, blockchain
from bson.objectid import ObjectId
import json

credential_bp = Blueprint('credentials', __name__, url_prefix='/api/credentials')

@credential_bp.route('/create', methods=['POST'])
@require_auth
def create_credential():
    """Create and store a new credential"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['credential_type', 'credential_data']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        user_id = request.user_id
        credential_type = data['credential_type']
        credential_data = data['credential_data']
        
        # Get user
        user = User.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Hash credential data for blockchain
        credential_hash = HashUtil.hash_credential(credential_data)
        
        # Encrypt sensitive data
        encryption_key = EncryptionUtil.generate_encryption_key()
        encrypted_data = EncryptionUtil.encrypt_data(json.dumps(credential_data), encryption_key)
        
        # Create credential in MongoDB
        credential_id = Credential.create_credential(
            user_id,
            credential_type,
            {
                'encrypted_data': encrypted_data,
                'encryption_key': encryption_key.decode() if isinstance(encryption_key, bytes) else encryption_key
            },
            credential_hash
        )
        
        # Try to store on blockchain if contract is available
        blockchain_tx = None
        if blockchain.contract:
            try:
                # Convert hash string to bytes32
                hash_bytes = bytes.fromhex(credential_hash.replace('0x', ''))
                if len(hash_bytes) < 32:
                    hash_bytes = hash_bytes + b'\x00' * (32 - len(hash_bytes))
                hash_bytes32 = hash_bytes[:32]
                
                blockchain_tx = blockchain.store_credential_hash(
                    user['wallet_address'],
                    hash_bytes32,
                    credential_type
                )
            except Exception as e:
                print(f"Warning: Could not store on blockchain: {str(e)}")
        
        return jsonify({
            'message': 'Credential created successfully',
            'credential_id': str(credential_id),
            'credential_hash': credential_hash,
            'blockchain_tx': blockchain_tx
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@credential_bp.route('/list', methods=['GET'])
@require_auth
def list_credentials():
    """List all credentials of a user"""
    try:
        user_id = request.user_id
        
        credentials = Credential.get_user_credentials(user_id)
        
        # Sanitize response (don't expose encryption keys)
        credentials_list = []
        for cred in credentials:
            credentials_list.append({
                'credential_id': str(cred['_id']),
                'credential_type': cred['credential_type'],
                'blockchain_hash': cred['blockchain_hash'],
                'created_at': cred['created_at'].isoformat(),
                'access_count': cred['access_count']
            })
        
        return jsonify({
            'credentials': credentials_list,
            'total': len(credentials_list)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@credential_bp.route('/<credential_id>', methods=['GET'])
@require_auth
def get_credential(credential_id):
    """Get a specific credential"""
    try:
        credential = Credential.get_credential_by_id(credential_id)
        
        if not credential:
            return jsonify({'error': 'Credential not found'}), 404
        
        # Check ownership
        if str(credential['user_id']) != request.user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Increment access count
        Credential.increment_access_count(credential_id)
        
        return jsonify({
            'credential_id': str(credential['_id']),
            'credential_type': credential['credential_type'],
            'blockchain_hash': credential['blockchain_hash'],
            'created_at': credential['created_at'].isoformat(),
            'access_count': credential['access_count']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@credential_bp.route('/<credential_hash>/blockchain-proof', methods=['GET'])
def get_blockchain_proof(credential_hash):
    """Get proof that credential exists on blockchain"""
    try:
        credential = Credential.get_credential_by_blockchain_hash(credential_hash)
        
        if not credential:
            return jsonify({'error': 'Credential not found'}), 404
        
        proof = {
            'credential_hash': credential['blockchain_hash'],
            'credential_type': credential['credential_type'],
            'created_at': credential['created_at'].isoformat(),
            'is_active': credential['is_active'],
            'blockchain_proof': None
        }
        
        # Try to get proof from blockchain contract
        if blockchain.contract:
            try:
                # Convert hash string to bytes32
                hash_bytes = bytes.fromhex(credential_hash.replace('0x', ''))
                if len(hash_bytes) < 32:
                    hash_bytes = hash_bytes + b'\x00' * (32 - len(hash_bytes))
                hash_bytes32 = hash_bytes[:32]
                
                # Get owner from contract
                owner = blockchain.contract.functions.getCredentialOwner(hash_bytes32).call()
                
                proof['blockchain_proof'] = {
                    'owner_address': owner,
                    'contract_address': str(blockchain.contract.address),
                    'network': 'Ethereum (Remix VM)',
                    'verified_on_chain': owner != '0x0000000000000000000000000000000000000000'
                }
            except Exception as e:
                print(f"Warning: Could not get blockchain proof: {str(e)}")
                proof['blockchain_proof'] = {
                    'error': str(e),
                    'contract_address': str(blockchain.contract_address) if blockchain.contract_address else None
                }
        
        return jsonify(proof), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    """Revoke a credential"""
    try:
        credential = Credential.get_credential_by_id(credential_id)
        
        if not credential:
            return jsonify({'error': 'Credential not found'}), 404
        
        # Check ownership
        if str(credential['user_id']) != request.user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Revoke credential
        Credential.revoke_credential(credential_id)
        
        return jsonify({
            'message': 'Credential revoked successfully',
            'credential_id': credential_id
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@credential_bp.route('/verify/<credential_hash>', methods=['GET'])
def verify_credential(credential_hash):
    """Verify a credential by its hash"""
    try:
        credential = Credential.get_credential_by_blockchain_hash(credential_hash)
        
        if not credential:
            return jsonify({'error': 'Credential not found'}), 404
        
        # Try to verify on blockchain
        blockchain_result = None
        if blockchain.contract:
            try:
                # Convert hash string to bytes32
                hash_bytes = bytes.fromhex(credential_hash.replace('0x', ''))
                if len(hash_bytes) < 32:
                    hash_bytes = hash_bytes + b'\x00' * (32 - len(hash_bytes))
                hash_bytes32 = hash_bytes[:32]
                
                # Get the owner from the credential record
                user = User.get_user_by_id(credential['user_id'])
                if user:
                    is_valid = blockchain.verify_credential(user['wallet_address'], hash_bytes32)
                    blockchain_result = {'valid': is_valid, 'source': 'blockchain'}
            except Exception as e:
                print(f"Warning: Could not verify on blockchain: {str(e)}")
        
        return jsonify({
            'valid': credential['is_active'],
            'credential_type': credential['credential_type'],
            'blockchain_hash': credential['blockchain_hash'],
            'created_at': credential['created_at'].isoformat(),
            'blockchain_verification': blockchain_result
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
