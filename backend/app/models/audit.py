from pymongo import MongoClient
from app.models.database import access_logs_collection
from datetime import datetime
from bson.objectid import ObjectId


class AuditLog:
    """Audit logging for credential access"""
    
    @staticmethod
    def log_access(user_id, credential_id, action, ip_address=None, status="success"):
        """Log credential access or verification"""
        log_data = {
            "user_id": ObjectId(user_id) if user_id else None,
            "credential_id": ObjectId(credential_id) if credential_id else None,
            "action": action,  # "view", "revoke", "verify", "share", etc.
            "ip_address": ip_address,
            "status": status,
            "timestamp": datetime.utcnow()
        }
        result = access_logs_collection.insert_one(log_data)
        return result.inserted_id
    
    @staticmethod
    def get_user_access_logs(user_id, limit=100):
        """Get access logs for a user"""
        return list(access_logs_collection.find(
            {"user_id": ObjectId(user_id)}
        ).sort("timestamp", -1).limit(limit))
    
    @staticmethod
    def get_credential_access_logs(credential_id):
        """Get access logs for a credential"""
        return list(access_logs_collection.find(
            {"credential_id": ObjectId(credential_id)}
        ).sort("timestamp", -1))
