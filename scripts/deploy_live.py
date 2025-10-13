#!/usr/bin/env python3
from web3 import Web3
import os
import json

def load_environment():
    """Load environment variables"""
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
        print("❌ .anonymous_env file not found")
        return {}

def deploy_contract():
    # Load environment
    env = load_environment()
    ANON_PUBLIC_KEY = env.get('export ANON_PUBLIC_KEY', '').replace('export ', '')
    ANON_PRIVATE_KEY = env.get('export ANON_PRIVATE_KEY', '').replace('export ', '')
    
    if not ANON_PUBLIC_KEY or not ANON_PRIVATE_KEY:
        print("❌ Could not load keys from .anonymous_env")
        return
    
    # Connect to Polygon Mainnet
    w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
    
    if not w3.is_connected():
        print("❌ Failed to connect to Polygon")
        return
    
    print(f"✅ Connected to Polygon Mainnet")
    print(f"📦 Deploying from: {ANON_PUBLIC_KEY}")
    
    # Check balance
    balance = w3.eth.get_balance(ANON_PUBLIC_KEY)
    balance_matic = w3.from_wei(balance, 'ether')
    print(f"💰 Balance: {balance_matic:.4f} MATIC")
    
    if balance == 0:
        print("\n❌ INSUFFICIENT MATIC FOR GAS")
        print(f"Please send MATIC to: {ANON_PUBLIC_KEY}")
        print("Need approximately 0.1-0.2 MATIC for deployment")
        return
    
    deployment_info = {
        'network': 'Polygon Mainnet',
        'deployer': ANON_PUBLIC_KEY,
        'creator_share': '3%',
        'community_share': '97%',
        'veto_period': '2 years',
        'gas_estimate': '0.1-0.2 MATIC',
        'status': 'READY_FOR_FULL_DEPLOYMENT'
    }
    
    print("📜 DEPLOYMENT READY:")
    print(json.dumps(deployment_info, indent=2))
    
    if balance_matic < 0.1:
        print(f"\n⚠️  Low balance: {balance_matic:.4f} MATIC")
        print("   Recommend sending more MATIC for deployment")
    else:
        print(f"\n✅ Sufficient balance for deployment: {balance_matic:.4f} MATIC")
        print("   Ready for full contract deployment")

if __name__ == "__main__":
    deploy_contract()
