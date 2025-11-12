# Blockchain deployment helpers and utilities

import json
from web3 import Web3

# Smart Contract ABI (Application Binary Interface)
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_userAddress", "type": "address"},
            {"internalType": "bytes32", "name": "_credentialHash", "type": "bytes32"},
            {"internalType": "string", "name": "_credentialType", "type": "string"}
        ],
        "name": "storeCredential",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_userAddress", "type": "address"},
            {"internalType": "bytes32", "name": "_credentialHash", "type": "bytes32"}
        ],
        "name": "verifyCredential",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_userAddress", "type": "address"},
            {"internalType": "bytes32", "name": "_credentialHash", "type": "bytes32"}
        ],
        "name": "revokeCredential",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Solidity source code for deployment
SOLIDITY_SOURCE = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title IdentityVerification
 * @dev Decentralized Identity Verification Smart Contract
 */
contract IdentityVerification {
    
    // Struct for storing credential information
    struct Credential {
        bytes32 credentialHash;
        string credentialType;
        uint256 timestamp;
        bool isActive;
    }
    
    // Struct for storing user credentials
    struct UserCredentials {
        address userAddress;
        bytes32[] credentialHashes;
        mapping(bytes32 => Credential) credentials;
        uint256 credentialCount;
    }
    
    // State variables
    mapping(address => UserCredentials) public users;
    mapping(bytes32 => address) public credentialToUser;
    
    address public owner;
    uint256 public totalCredentials;
    
    // Events
    event CredentialStored(
        address indexed userAddress,
        bytes32 indexed credentialHash,
        string credentialType,
        uint256 timestamp
    );
    
    event CredentialRevoked(
        address indexed userAddress,
        bytes32 indexed credentialHash,
        uint256 timestamp
    );
    
    // Constructor
    constructor() {
        owner = msg.sender;
        totalCredentials = 0;
    }
    
    function storeCredential(
        address _userAddress,
        bytes32 _credentialHash,
        string memory _credentialType
    ) public {
        require(_userAddress != address(0), "Invalid user address");
        require(_credentialHash != bytes32(0), "Invalid credential hash");
        require(credentialToUser[_credentialHash] == address(0), "Credential already exists");
        
        Credential memory newCredential = Credential({
            credentialHash: _credentialHash,
            credentialType: _credentialType,
            timestamp: block.timestamp,
            isActive: true
        });
        
        users[_userAddress].credentials[_credentialHash] = newCredential;
        users[_userAddress].credentialHashes.push(_credentialHash);
        users[_userAddress].credentialCount++;
        
        credentialToUser[_credentialHash] = _userAddress;
        totalCredentials++;
        
        emit CredentialStored(_userAddress, _credentialHash, _credentialType, block.timestamp);
    }
    
    function verifyCredential(address _userAddress, bytes32 _credentialHash)
        public
        view
        returns (bool)
    {
        if (credentialToUser[_credentialHash] != _userAddress) {
            return false;
        }
        
        Credential storage cred = users[_userAddress].credentials[_credentialHash];
        return cred.isActive && cred.credentialHash == _credentialHash;
    }
    
    function revokeCredential(address _userAddress, bytes32 _credentialHash)
        public
    {
        require(credentialToUser[_credentialHash] == _userAddress, "Credential does not belong to user");
        
        Credential storage cred = users[_userAddress].credentials[_credentialHash];
        cred.isActive = false;
        
        emit CredentialRevoked(_userAddress, _credentialHash, block.timestamp);
    }
    
    function getTotalCredentials() public view returns (uint256) {
        return totalCredentials;
    }
}
"""


def save_contract_abi(filepath):
    """Save contract ABI to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(CONTRACT_ABI, f, indent=2)


def load_contract_abi(filepath):
    """Load contract ABI from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)
