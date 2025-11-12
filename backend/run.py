from flask import Flask, jsonify
from flask_cors import CORS
from app.models.database import create_indexes
from app.routes import auth_bp, credential_bp, user_bp
from app.utils import blockchain
import os
from dotenv import load_dotenv
import json

load_dotenv()

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize database indexes
    try:
        create_indexes()
        print("Database indexes created successfully")
    except Exception as e:
        print(f"Warning: Could not create indexes: {str(e)}")
    
    # Initialize smart contract
    try:
        abi_path = os.path.join(os.path.dirname(__file__), '..', 'smart-contracts', 'IdentityVerification.abi.json')
        with open(abi_path, 'r') as f:
            abi = json.load(f)
        blockchain.initialize_contract(abi)
        if blockchain.contract:
            print(f"Smart contract initialized at {blockchain.contract_address}")
        else:
            print("Warning: Contract not initialized (no address configured)")
    except Exception as e:
        print(f"Warning: Could not initialize smart contract: {str(e)}")
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(credential_bp)
    app.register_blueprint(user_bp)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Decentralized Identity Verification System'
        }), 200

    @app.route('/api/blockchain/status', methods=['GET'])
    def blockchain_status():
        try:
            status = {
                'connected': blockchain.is_connected(),
                'has_contract': bool(blockchain.contract),
                'contract_address': getattr(blockchain.contract, 'address', None) if blockchain.contract else None,
                'provider': getattr(blockchain.w3.provider, 'endpoint_uri', None)
            }
            return jsonify(status), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=True)
