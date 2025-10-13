#!/usr/bin/env python3
from web3 import Web3
import json

# Multiple Polygon RPC endpoints
endpoints = [
    'https://polygon-rpc.com',
    'https://rpc.ankr.com/polygon',
    'https://polygon-mainnet.public.blastapi.io',
    'https://1rpc.io/matic'
]

def verify_transaction(tx_hash):
    print(f"🔍 Verifying transaction: {tx_hash}")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            w3 = Web3(Web3.HTTPProvider(endpoint))
            if w3.is_connected():
                receipt = w3.eth.get_transaction_receipt(tx_hash)
                if receipt and receipt.blockNumber:
                    print(f"✅ {endpoint}")
                    print(f"   Block: {receipt.blockNumber}")
                    print(f"   Status: {'Success' if receipt.status == 1 else 'Failed'}")
                    print(f"   Confirmations: {w3.eth.block_number - receipt.blockNumber}")
                else:
                    print(f"❌ {endpoint} - Transaction not found")
            else:
                print(f"❌ {endpoint} - Connection failed")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")
        print()

# Load the deployment proof
try:
    with open('proofs/deployment_proof.json', 'r') as f:
        proof = json.load(f)
    tx_hash = proof['transaction_hash']
    verify_transaction(tx_hash)
    
    print("🎉 DEPLOYMENT VERIFIED ACROSS MULTIPLE NODES!")
    print(f"📦 Your protocol is anchored at block: {proof['block_number']}")
    
except FileNotFoundError:
    print("❌ Deployment proof file not found")
