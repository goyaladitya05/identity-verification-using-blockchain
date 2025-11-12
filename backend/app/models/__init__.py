from datetime import datetime
from .database import users_collection, credentials_collection
import hashlib
from bson.objectid import ObjectId

class User:
    """User model for identity verification system"""
    
    @staticmethod
    def create_user(email, wallet_address, full_name, password_hash):
        """Create a new user"""
        user_data = {
            "email": email,
            "wallet_address": wallet_address,
            "full_name": full_name,
            "password_hash": password_hash,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_verified": False,
            "credentials": [],
            "verification_count": 0
        }
        result = users_collection.insert_one(user_data)
        return result.inserted_id
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return users_collection.find_one({"email": email})
    
    @staticmethod
    def get_user_by_wallet(wallet_address):
        """Get user by wallet address"""
        return users_collection.find_one({"wallet_address": wallet_address})
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return users_collection.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def update_user(user_id, update_data):
        """Update user information"""
        update_data["updated_at"] = datetime.utcnow()
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def mark_verified(user_id):
        """Mark user as verified"""
        return User.update_user(user_id, {"is_verified": True})


class Credential:
    """Credential model for storing identity credentials"""
    
    @staticmethod
    def create_credential(user_id, credential_type, data, blockchain_hash):
        """Create a new credential"""
        credential_data = {
            "user_id": ObjectId(user_id),
            "credential_type": credential_type,  # passport, aadhar, drivers_license, etc.
            "data": data,  # Encrypted credential data
            "blockchain_hash": blockchain_hash,
            "blockchain_timestamp": datetime.utcnow(),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True,
            "access_count": 0
        }
        result = credentials_collection.insert_one(credential_data)
        return result.inserted_id
    
    @staticmethod
    def get_credential_by_id(credential_id):
        """Get credential by ID"""
        return credentials_collection.find_one({"_id": ObjectId(credential_id)})
    
    @staticmethod
    def get_user_credentials(user_id):
        """Get all credentials of a user"""
        return list(credentials_collection.find(
            {"user_id": ObjectId(user_id), "is_active": True}
        ))
    
    @staticmethod
    def get_credential_by_blockchain_hash(blockchain_hash):
        """Get credential by blockchain hash"""
        return credentials_collection.find_one({"blockchain_hash": blockchain_hash})
    
    @staticmethod
    def increment_access_count(credential_id):
        """Increment access count for audit purposes"""
        credentials_collection.update_one(
            {"_id": ObjectId(credential_id)},
            {"$inc": {"access_count": 1}, "$set": {"updated_at": datetime.utcnow()}}
        )
    
    @staticmethod
    def revoke_credential(credential_id):
        """Revoke a credential"""
        credentials_collection.update_one(
            {"_id": ObjectId(credential_id)},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
