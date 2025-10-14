// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.19;

/**
 * @title ImageAttachments
 * @dev Encrypted lyric diary system with version control
 * Phase 3: Sovereign Identity & Protection  
 */
contract ImageAttachments {
    struct Attachment {
        string ipfsHash;
        bytes32 contentHash;
        uint256 timestamp;
        string attachmentType; // "lyric", "sheet_music", "handwritten"
        string description;
        string previousVersionHash; // For version chain
    }
    
    mapping(address => Attachment[]) public creatorAttachments;
    
    event AttachmentCreated(
        address indexed creator,
        string ipfsHash,
        string attachmentType,
        uint256 timestamp
    );
    
    function createAttachment(
        string calldata ipfsHash,
        bytes32 contentHash,
        string calldata attachmentType,
        string calldata description,
        string calldata previousVersionHash
    ) external {
        creatorAttachments[msg.sender].push(Attachment({
            ipfsHash: ipfsHash,
            contentHash: contentHash,
            timestamp: block.timestamp,
            attachmentType: attachmentType,
            description: description,
            previousVersionHash: previousVersionHash
        }));
        
        emit AttachmentCreated(msg.sender, ipfsHash, attachmentType, block.timestamp);
    }
    
    function getAttachments(address creator) public view returns (Attachment[] memory) {
        return creatorAttachments[creator];
    }
}
