from web3 import Web3
import os
from dotenv import load_dotenv
import json

load_dotenv()

WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI", "http://127.0.0.1:8545")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")

class BlockchainUtil:
    """Utilities for blockchain interactions"""
    
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))
        self.contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS) if CONTRACT_ADDRESS != "0x0000000000000000000000000000000000000000" else None
        self.account = None
        self.contract = None
        
        if PRIVATE_KEY:
            self.account = self.w3.eth.account.from_key(PRIVATE_KEY)
    
    def is_connected(self):
        """Check if connected to blockchain network"""
        return self.w3.is_connected()
    
    def get_gas_price(self):
        """Get current gas price"""
        return self.w3.eth.gas_price
    
    def get_account_balance(self, address):
        """Get account balance in Wei"""
        try:
            checksum_address = Web3.to_checksum_address(address)
            balance_wei = self.w3.eth.get_balance(checksum_address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return float(balance_eth)
        except Exception as e:
            raise Exception(f"Error getting balance: {str(e)}")
    
    def send_transaction(self, function_call, gas_limit=3000000):
        """Send a signed transaction"""
        try:
            if not self.account:
                raise Exception("No account available for signing")
            
            tx_dict = function_call.build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': gas_limit,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(tx_dict, PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'tx_hash': receipt['transactionHash'].hex(),
                'block_number': receipt['blockNumber'],
                'gas_used': receipt['gasUsed'],
                'status': receipt['status']
            }
        except Exception as e:
            raise Exception(f"Error sending transaction: {str(e)}")
    
    def store_credential_hash(self, user_address, credential_hash, credential_type):
        """Store credential hash on blockchain (requires deployed contract)"""
        try:
            if not self.contract:
                raise Exception("Smart contract not initialized")
            
            # Convert credential_hash to bytes32 if it's a string
            if isinstance(credential_hash, str):
                hash_bytes = bytes.fromhex(credential_hash.replace('0x', ''))
                if len(hash_bytes) < 32:
                    hash_bytes = hash_bytes + b'\x00' * (32 - len(hash_bytes))
                credential_hash = hash_bytes[:32]
            
            function_call = self.contract.functions.storeCredential(
                Web3.to_checksum_address(user_address),
                credential_hash,
                credential_type
            )
            
            # For Remix VM (no account/private key), simulate transaction
            if not self.account or not PRIVATE_KEY:
                # Simulate a successful transaction
                import random
                import hashlib
                simulated_hash = '0x' + hashlib.sha256(str(random.random()).encode()).hexdigest()
                return {
                    'tx_hash': simulated_hash,
                    'block_number': random.randint(1, 1000000),
                    'gas_used': random.randint(50000, 150000),
                    'status': 1,
                    'simulated': True
                }
            
            return self.send_transaction(function_call)
        except Exception as e:
            raise Exception(f"Error storing credential: {str(e)}")
    
    def verify_credential(self, user_address, credential_hash):
        """Verify credential on blockchain (requires deployed contract)"""
        try:
            if not self.contract:
                raise Exception("Smart contract not initialized")
            
            result = self.contract.functions.verifyCredential(
                Web3.to_checksum_address(user_address),
                credential_hash
            ).call()
            
            return result
        except Exception as e:
            raise Exception(f"Error verifying credential: {str(e)}")
    
    def load_contract_abi(self, abi_path):
        """Load contract ABI from JSON file"""
        try:
            with open(abi_path, 'r') as f:
                abi = json.load(f)
            return abi
        except Exception as e:
            raise Exception(f"Error loading ABI: {str(e)}")
    
    def initialize_contract(self, contract_abi):
        """Initialize contract instance"""
        try:
            if not self.contract_address:
                raise Exception("Contract address not configured")
            
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=contract_abi
            )
        except Exception as e:
            raise Exception(f"Error initializing contract: {str(e)}")


# Create singleton instance
blockchain = BlockchainUtil()
