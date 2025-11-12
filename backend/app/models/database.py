from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "identity_verification")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# Collections
users_collection = db["users"]
credentials_collection = db["credentials"]
verifications_collection = db["verifications"]
access_logs_collection = db["access_logs"]

# Create indexes for better query performance
def create_indexes():
    users_collection.create_index("email", unique=True)
    users_collection.create_index("wallet_address", unique=True)
    credentials_collection.create_index("user_id")
    credentials_collection.create_index("blockchain_hash")
    verifications_collection.create_index("user_id")
    verifications_collection.create_index("verifier_address")
    access_logs_collection.create_index("user_id")
    access_logs_collection.create_index("timestamp")
