// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Universal Resource Code (URC) Registry
 * @dev Central registry for unified resource identification across the NOVA ecosystem
 * @notice Master identifier system for all digital assets, tokens, and contracts
 */

contract URCRegistry {
    // ========== Structures ==========
    
    struct UniversalResource {
        string urc;                    // Master URC identifier
        string resourceId;             // RID-XXXXXX
        string tokenId;                // NTK-XXXXXX
        string walletId;               // NWA-XXXXXX
        string contractId;             // NCT-XXXXXX
        string governanceId;           // NDAO-XXXX
        
        string name;
        string resourceType;           // digital_asset, token, contract, etc.
        
        address owner;
        uint256 createdAt;
        uint256 updatedAt;
        
        string verificationAlgorithm;  // SHA-256, KECCAK-256, etc.
        bool verified;
        bytes32 verificationHash;
        
        string network;
        string consensus;              // ProofOfStake, ProofOfWork, etc.
        
        bool active;
    }

    struct ResourceMetadata {
        string key;
        string value;
    }

    // ========== Storage ==========
    
    mapping(string => UniversalResource) public resources;      // URC -> Resource
    mapping(address => string[]) public userResources;          // User -> URC[]
    mapping(string => ResourceMetadata[]) public metadata;      // URC -> Metadata[]
    mapping(string => bool) public urcExists;                   // URC existence check
    mapping(string => string) public ridToURC;                  // RID -> URC mapping
    mapping(string => string) public tokenToURC;                // Token ID -> URC mapping
    mapping(string => string) public contractToURC;             // Contract ID -> URC mapping
    
    uint256 public resourceCount;
    address public owner;
    
    // ========== Events ==========
    
    event ResourceRegistered(
        string indexed urc,
        string indexed resourceId,
        address indexed owner,
        uint256 timestamp
    );
    
    event ResourceVerified(
        string indexed urc,
        bytes32 verificationHash,
        uint256 timestamp
    );
    
    event ResourceUpdated(
        string indexed urc,
        uint256 timestamp
    );
    
    event URCLinked(
        string indexed urc,
        string resourceId,
        string tokenId,
        string walletId,
        string contractId,
        string governanceId
    );

    // ========== Modifiers ==========
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }

    modifier resourceExists(string memory _urc) {
        require(urcExists[_urc], "Resource does not exist");
        _;
    }

    modifier onlyResourceOwner(string memory _urc) {
        require(
            msg.sender == resources[_urc].owner || msg.sender == owner,
            "Only resource owner can call this"
        );
        _;
    }

    // ========== Constructor ==========
    
    constructor() {
        owner = msg.sender;
        resourceCount = 0;
    }

    // ========== Registration Functions ==========

    /**
     * @dev Register a new universal resource
     * @param _urc Master URC identifier (SHA-256 hash)
     * @param _resourceId Resource ID (RID-XXXXXX)
     * @param _tokenId Token ID (NTK-XXXXXX)
     * @param _walletId Wallet ID (NWA-XXXXXX)
     * @param _contractId Contract ID (NCT-XXXXXX)
     * @param _governanceId Governance ID (NDAO-XXXX)
     * @param _name Resource name
     * @param _type Resource type
     */
    function registerResource(
        string memory _urc,
        string memory _resourceId,
        string memory _tokenId,
        string memory _walletId,
        string memory _contractId,
        string memory _governanceId,
        string memory _name,
        string memory _type
    ) public returns (bool) {
        require(!urcExists[_urc], "URC already exists");
        require(bytes(_urc).length == 64, "Invalid URC format"); // SHA-256 hex
        require(bytes(_resourceId).length > 0, "Resource ID cannot be empty");

        UniversalResource storage resource = resources[_urc];
        
        resource.urc = _urc;
        resource.resourceId = _resourceId;
        resource.tokenId = _tokenId;
        resource.walletId = _walletId;
        resource.contractId = _contractId;
        resource.governanceId = _governanceId;
        resource.name = _name;
        resource.resourceType = _type;
        resource.owner = msg.sender;
        resource.createdAt = block.timestamp;
        resource.updatedAt = block.timestamp;
        resource.verificationAlgorithm = "SHA-256";
        resource.verified = false;
        resource.network = "Ethereum";
        resource.consensus = "ProofOfStake";
        resource.active = true;

        urcExists[_urc] = true;
        ridToURC[_resourceId] = _urc;
        
        if (bytes(_tokenId).length > 0) {
            tokenToURC[_tokenId] = _urc;
        }
        if (bytes(_contractId).length > 0) {
            contractToURC[_contractId] = _urc;
        }

        userResources[msg.sender].push(_urc);
        resourceCount++;

        emit ResourceRegistered(_urc, _resourceId, msg.sender, block.timestamp);
        emit URCLinked(
            _urc,
            _resourceId,
            _tokenId,
            _walletId,
            _contractId,
            _governanceId
        );

        return true;
    }

    /**
     * @dev Verify resource with cryptographic hash
     * @param _urc Master URC identifier
     * @param _verificationHash SHA-256 hash of resource data
     */
    function verifyResource(
        string memory _urc,
        bytes32 _verificationHash
    ) public onlyResourceOwner(_urc) resourceExists(_urc) returns (bool) {
        UniversalResource storage resource = resources[_urc];
        
        resource.verificationHash = _verificationHash;
        resource.verified = true;
        resource.updatedAt = block.timestamp;

        emit ResourceVerified(_urc, _verificationHash, block.timestamp);
        return true;
    }

    /**
     * @dev Add metadata to resource
     * @param _urc Master URC identifier
     * @param _key Metadata key
     * @param _value Metadata value
     */
    function addMetadata(
        string memory _urc,
        string memory _key,
        string memory _value
    ) public onlyResourceOwner(_urc) resourceExists(_urc) returns (bool) {
        require(bytes(_key).length > 0, "Key cannot be empty");
        
        metadata[_urc].push(ResourceMetadata(_key, _value));
        resources[_urc].updatedAt = block.timestamp;

        emit ResourceUpdated(_urc, block.timestamp);
        return true;
    }

    /**
     * @dev Deactivate resource
     * @param _urc Master URC identifier
     */
    function deactivateResource(
        string memory _urc
    ) public onlyResourceOwner(_urc) resourceExists(_urc) returns (bool) {
        resources[_urc].active = false;
        resources[_urc].updatedAt = block.timestamp;

        emit ResourceUpdated(_urc, block.timestamp);
        return true;
    }

    /**
     * @dev Reactivate resource
     * @param _urc Master URC identifier
     */
    function reactivateResource(
        string memory _urc
    ) public onlyResourceOwner(_urc) resourceExists(_urc) returns (bool) {
        resources[_urc].active = true;
        resources[_urc].updatedAt = block.timestamp;

        emit ResourceUpdated(_urc, block.timestamp);
        return true;
    }

    // ========== Query Functions ==========

    /**
     * @dev Get complete resource information
     * @param _urc Master URC identifier
     */
    function getResource(string memory _urc) 
        public 
        view 
        resourceExists(_urc) 
        returns (UniversalResource memory) 
    {
        return resources[_urc];
    }

    /**
     * @dev Get resource by RID
     * @param _rid Resource ID
     */
    function getResourceByRID(string memory _rid) 
        public 
        view 
        returns (UniversalResource memory) 
    {
        string memory urc = ridToURC[_rid];
        require(urcExists[urc], "Resource not found");
        return resources[urc];
    }

    /**
     * @dev Get resource by token ID
     * @param _tokenId Token ID
     */
    function getResourceByToken(string memory _tokenId) 
        public 
        view 
        returns (UniversalResource memory) 
    {
        string memory urc = tokenToURC[_tokenId];
        require(urcExists[urc], "Resource not found");
        return resources[urc];
    }

    /**
     * @dev Get resource by contract ID
     * @param _contractId Contract ID
     */
    function getResourceByContract(string memory _contractId) 
        public 
        view 
        returns (UniversalResource memory) 
    {
        string memory urc = contractToURC[_contractId];
        require(urcExists[urc], "Resource not found");
        return resources[urc];
    }

    /**
     * @dev Get all resources for an address
     * @param _address User address
     */
    function getUserResources(address _address) 
        public 
        view 
        returns (string[] memory) 
    {
        return userResources[_address];
    }

    /**
     * @dev Get metadata for resource
     * @param _urc Master URC identifier
     */
    function getMetadata(string memory _urc) 
        public 
        view 
        resourceExists(_urc) 
        returns (ResourceMetadata[] memory) 
    {
        return metadata[_urc];
    }

    /**
     * @dev Verify resource integrity
     * @param _urc Master URC identifier
     * @param _expectedHash Expected verification hash
     */
    function verifyIntegrity(
        string memory _urc,
        bytes32 _expectedHash
    ) public view resourceExists(_urc) returns (bool) {
        UniversalResource memory resource = resources[_urc];
        require(resource.verified, "Resource not verified");
        return resource.verificationHash == _expectedHash;
    }

    /**
     * @dev Get registry statistics
     */
    function getStats() public view returns (
        uint256 total,
        uint256 verified,
        uint256 active
    ) {
        uint256 verifiedCount = 0;
        uint256 activeCount = 0;

        // Note: In production, use pagination for large datasets
        // This is a simplified version
        
        return (resourceCount, verifiedCount, activeCount);
    }

    /**
     * @dev Check if URC exists
     * @param _urc Master URC identifier
     */
    function exists(string memory _urc) public view returns (bool) {
        return urcExists[_urc];
    }

    /**
     * @dev Check if resource is active
     * @param _urc Master URC identifier
     */
    function isActive(string memory _urc) public view returns (bool) {
        if (!urcExists[_urc]) return false;
        return resources[_urc].active;
    }

    /**
     * @dev Check if resource is verified
     * @param _urc Master URC identifier
     */
    function isVerified(string memory _urc) public view returns (bool) {
        if (!urcExists[_urc]) return false;
        return resources[_urc].verified;
    }

    // ========== Admin Functions ==========

    /**
     * @dev Transfer ownership
     * @param _newOwner New owner address
     */
    function transferOwnership(address _newOwner) public onlyOwner {
        require(_newOwner != address(0), "Invalid address");
        owner = _newOwner;
    }

    /**
     * @dev Emergency: Deactivate resource (owner only)
     * @param _urc Master URC identifier
     */
    function emergencyDeactivate(string memory _urc) 
        public 
        onlyOwner 
        resourceExists(_urc) 
        returns (bool) 
    {
        resources[_urc].active = false;
        resources[_urc].updatedAt = block.timestamp;
        return true;
    }
}
