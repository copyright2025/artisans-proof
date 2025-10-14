// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.19;

/**
 * @title SovereignIdentity
 * @dev Master identity registry for creators
 * Phase 3: Sovereign Identity & Protection
 */
contract SovereignIdentity {
    struct SovereignCreator {
        bytes32 fractalRootHash;      // Hash of signature-derived fractal seed
        bytes32 biologicalAnchor;     // Voiceprint hash
        address creatorAddress;
        uint256 identityCreationTime;
        string encryptedSignatureIPFS; // Optional: Encrypted signature image
        string sovereigntyPath;       // "legal", "creative", "biological", "digital"
    }
    
    mapping(address => SovereignCreator) public sovereignCreators;
    
    event SovereignIdentityCreated(
        address indexed creator,
        bytes32 fractalRootHash,
        string sovereigntyPath,
        uint256 timestamp
    );
    
    function createSovereignIdentity(
        bytes32 fractalRootHash,
        bytes32 biologicalHash,
        string calldata signatureIPFS,
        string calldata sovereigntyPath
    ) external {
        require(sovereignCreators[msg.sender].creatorAddress == address(0), 
                "Identity already exists");
        require(bytes(sovereigntyPath).length > 0, "Sovereignty path required");
        
        sovereignCreators[msg.sender] = SovereignCreator({
            fractalRootHash: fractalRootHash,
            biologicalAnchor: biologicalHash,
            creatorAddress: msg.sender,
            identityCreationTime: block.timestamp,
            encryptedSignatureIPFS: signatureIPFS,
            sovereigntyPath: sovereigntyPath
        });
        
        emit SovereignIdentityCreated(msg.sender, fractalRootHash, sovereigntyPath, block.timestamp);
    }
    
    function getIdentity(address creator) public view returns (SovereignCreator memory) {
        return sovereignCreators[creator];
    }
}
