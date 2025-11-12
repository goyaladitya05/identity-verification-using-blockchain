import hashlib
import secrets
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

# Encryption utilities
class EncryptionUtil:
    """Utilities for encrypting and decrypting sensitive data"""
    
    @staticmethod
    def generate_encryption_key():
        """Generate a new encryption key"""
        return Fernet.generate_key()
    
    @staticmethod
    def encrypt_data(data, key):
        """Encrypt data using Fernet symmetric encryption"""
        cipher = Fernet(key)
        encrypted = cipher.encrypt(data.encode() if isinstance(data, str) else data)
        return encrypted.decode()
    
    @staticmethod
    def decrypt_data(encrypted_data, key):
        """Decrypt data"""
        cipher = Fernet(key)
        decrypted = cipher.decrypt(encrypted_data.encode() if isinstance(encrypted_data, str) else encrypted_data)
        return decrypted.decode()
    
    @staticmethod
    def hash_data(data):
        """Hash data using SHA-256"""
        return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()
    
    @staticmethod
    def generate_salt(length=16):
        """Generate a random salt"""
        return secrets.token_hex(length)


# Hashing utilities
class HashUtil:
    """Utilities for generating hashes for blockchain"""
    
    @staticmethod
    def hash_credential(credential_data):
        """Create a hash of credential data for blockchain storage"""
        data_str = str(credential_data)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    @staticmethod
    def create_merkle_hash(hashes_list):
        """Create a Merkle root hash from a list of hashes"""
        if not hashes_list:
            return hashlib.sha256(b"").hexdigest()
        
        while len(hashes_list) > 1:
            new_hashes = []
            for i in range(0, len(hashes_list), 2):
                if i + 1 < len(hashes_list):
                    combined = hashes_list[i] + hashes_list[i + 1]
                else:
                    combined = hashes_list[i] + hashes_list[i]
                new_hashes.append(hashlib.sha256(combined.encode()).hexdigest())
            hashes_list = new_hashes
        
        return hashes_list[0]
