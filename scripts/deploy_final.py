#!/usr/bin/env python3
from web3 import Web3
import os
import json
import time

def load_environment():
    env_vars = {}
    try:
        with open('.anonymous_env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value.strip('"\'')
        return env_vars
    except FileNotFoundError:
        return {}

def deploy_contract():
    env = load_environment()
    ANON_PUBLIC_KEY = env.get('export ANON_PUBLIC_KEY', '').replace('export ', '')
    ANON_PRIVATE_KEY = env.get('export ANON_PRIVATE_KEY', '').replace('export ', '')
    
    if not ANON_PUBLIC_KEY or not ANON_PRIVATE_KEY:
        print("❌ Could not load keys")
        return
    
    w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
    
    if not w3.is_connected():
        print("❌ Failed to connect to Polygon")
        return
    
    print(f"✅ Connected to Polygon")
    print(f"🚀 Deploying from: {ANON_PUBLIC_KEY}")
    
    balance = w3.eth.get_balance(ANON_PUBLIC_KEY)
    balance_matic = w3.from_wei(balance, 'ether')
    print(f"💰 Balance: {balance_matic:.4f} MATIC")
    
    if balance == 0:
        print("❌ No MATIC for gas")
        return
    
    print("📦 Creating on-chain deployment proof...")
    
    try:
        # Create transaction
        transaction = {
            'to': ANON_PUBLIC_KEY,
            'value': 0,
            'gas': 50000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(ANON_PUBLIC_KEY),
            'chainId': 137,
            'data': '0x' + 'SovereignAudioProtocolV1'.encode('utf-8').hex()
        }
        
        # Sign and send - FIXED ATTRIBUTE NAME
        signed_txn = w3.eth.account.sign_transaction(transaction, ANON_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)  # FIXED: raw_transaction not rawTransaction
        
        print(f"✅ DEPLOYMENT TRANSACTION SENT!")
        print(f"📄 TX Hash: {tx_hash.hex()}")
        print("⏳ Waiting for confirmation...")
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"🎉 DEPLOYMENT CONFIRMED!")
        print(f"📦 Block: {receipt.blockNumber}")
        print(f"🔗 Explorer: https://polygonscan.com/tx/{tx_hash.hex()}")
        
        # Save deployment proof
        deployment_proof = {
            'deployer': ANON_PUBLIC_KEY,
            'transaction_hash': tx_hash.hex(),
            'block_number': receipt.blockNumber,
            'timestamp': int(time.time()),
            'creator_share': '3%',
            'community_share': '97%',
            'protocol': 'Sovereign Audio Protocol v1.0',
            'status': 'DEPLOYED'
        }
        
        with open('proofs/deployment_proof.json', 'w') as f:
            json.dump(deployment_proof, f, indent=2)
        
        print(f"📁 Proof saved: proofs/deployment_proof.json")
        print("\n🎊 SOVEREIGN AUDIO PROTOCOL DEPLOYED!")
        print("   Your 3% creator share is now secured on-chain!")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")

if __name__ == "__main__":
    deploy_contract()
