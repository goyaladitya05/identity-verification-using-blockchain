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
    
    event CredentialVerified(
        address indexed userAddress,
        bytes32 indexed credentialHash,
        bool isValid
    );
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier credentialExists(bytes32 _credentialHash) {
        require(credentialToUser[_credentialHash] != address(0), "Credential does not exist");
        _;
    }
    
    // Constructor
    constructor() {
        owner = msg.sender;
        totalCredentials = 0;
    }
    
    /**
     * @dev Store a credential on the blockchain
     * @param _userAddress Address of the user
     * @param _credentialHash Hash of the credential
     * @param _credentialType Type of credential (e.g., "passport", "aadhar")
     */
    function storeCredential(
        address _userAddress,
        bytes32 _credentialHash,
        string memory _credentialType
    ) public {
        require(_userAddress != address(0), "Invalid user address");
        require(_credentialHash != bytes32(0), "Invalid credential hash");
        require(bytes(_credentialType).length > 0, "Invalid credential type");
        require(credentialToUser[_credentialHash] == address(0), "Credential already exists");
        
        // Create new credential
        Credential memory newCredential = Credential({
            credentialHash: _credentialHash,
            credentialType: _credentialType,
            timestamp: block.timestamp,
            isActive: true
        });
        
        // Store credential
        users[_userAddress].credentials[_credentialHash] = newCredential;
        users[_userAddress].credentialHashes.push(_credentialHash);
        users[_userAddress].credentialCount++;
        
        credentialToUser[_credentialHash] = _userAddress;
        totalCredentials++;
        
        emit CredentialStored(_userAddress, _credentialHash, _credentialType, block.timestamp);
    }
    
    /**
     * @dev Verify if a credential exists and is valid
     * @param _userAddress Address of the user
     * @param _credentialHash Hash of the credential
     * @return bool True if credential is valid, false otherwise
     */
    function verifyCredential(address _userAddress, bytes32 _credentialHash)
        public
        returns (bool)
    {
        require(_userAddress != address(0), "Invalid user address");
        require(_credentialHash != bytes32(0), "Invalid credential hash");
        
        if (credentialToUser[_credentialHash] != _userAddress) {
            emit CredentialVerified(_userAddress, _credentialHash, false);
            return false;
        }
        
        Credential storage cred = users[_userAddress].credentials[_credentialHash];
        bool isValid = cred.isActive && cred.credentialHash == _credentialHash;
        
        emit CredentialVerified(_userAddress, _credentialHash, isValid);
        return isValid;
    }
    
    /**
     * @dev Revoke a credential
     * @param _userAddress Address of the user
     * @param _credentialHash Hash of the credential
     */
    function revokeCredential(address _userAddress, bytes32 _credentialHash)
        public
        credentialExists(_credentialHash)
    {
        require(_userAddress != address(0), "Invalid user address");
        require(credentialToUser[_credentialHash] == _userAddress, "Credential does not belong to user");
        
        Credential storage cred = users[_userAddress].credentials[_credentialHash];
        cred.isActive = false;
        
        emit CredentialRevoked(_userAddress, _credentialHash, block.timestamp);
    }
    
    /**
     * @dev Get credential details
     * @param _userAddress Address of the user
     * @param _credentialHash Hash of the credential
     * @return Credential details
     */
    function getCredential(address _userAddress, bytes32 _credentialHash)
        public
        view
        credentialExists(_credentialHash)
        returns (bytes32, string memory, uint256, bool)
    {
        require(credentialToUser[_credentialHash] == _userAddress, "Credential does not belong to user");
        
        Credential storage cred = users[_userAddress].credentials[_credentialHash];
        return (cred.credentialHash, cred.credentialType, cred.timestamp, cred.isActive);
    }
    
    /**
     * @dev Get user's credential count
     * @param _userAddress Address of the user
     * @return Number of credentials
     */
    function getUserCredentialCount(address _userAddress)
        public
        view
        returns (uint256)
    {
        return users[_userAddress].credentialCount;
    }
    
    /**
     * @dev Get user's credentials
     * @param _userAddress Address of the user
     * @return Array of credential hashes
     */
    function getUserCredentials(address _userAddress)
        public
        view
        returns (bytes32[] memory)
    {
        return users[_userAddress].credentialHashes;
    }
    
    /**
     * @dev Get owner of a credential
     * @param _credentialHash Hash of the credential
     * @return Address of the credential owner
     */
    function getCredentialOwner(bytes32 _credentialHash)
        public
        view
        returns (address)
    {
        return credentialToUser[_credentialHash];
    }
    
    /**
     * @dev Get total credentials on blockchain
     * @return Total number of credentials
     */
    function getTotalCredentials() public view returns (uint256) {
        return totalCredentials;
    }
}
