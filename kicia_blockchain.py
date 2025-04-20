# kicia_blockchain.py
"""
Moduł do wdrażania smart kontraktów na Polygon, Binance Smart Chain i Solana.
Wymaga bibliotek: web3, solana, python-dotenv (do obsługi kluczy).
"""
from typing import Optional

def deploy_contract_polygon(bytecode: str, abi: list, private_key: str, rpc_url: str) -> Optional[str]:
    """Wdraża kontrakt na Polygon (EVM, web3.py). Zwraca adres kontraktu lub None."""
    try:
        from web3 import Web3
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        acct = w3.eth.account.from_key(private_key)
        Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx = Contract.constructor().build_transaction({
            'from': acct.address,
            'nonce': w3.eth.get_transaction_count(acct.address),
            'gas': 2000000,
            'gasPrice': w3.to_wei('5', 'gwei')
        })
        signed = acct.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.contractAddress
    except Exception as e:
        print(f"Błąd wdrażania kontraktu na Polygon: {e}")
        return None

def deploy_contract_bsc(bytecode: str, abi: list, private_key: str, rpc_url: str) -> Optional[str]:
    """Wdraża kontrakt na Binance Smart Chain (EVM, web3.py). Zwraca adres kontraktu lub None."""
    try:
        from web3 import Web3
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        acct = w3.eth.account.from_key(private_key)
        Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx = Contract.constructor().build_transaction({
            'from': acct.address,
            'nonce': w3.eth.get_transaction_count(acct.address),
            'gas': 2000000,
            'gasPrice': w3.to_wei('5', 'gwei')
        })
        signed = acct.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.contractAddress
    except Exception as e:
        print(f"Błąd wdrażania kontraktu na BSC: {e}")
        return None

def deploy_contract_solana(program_path: str, keypair_path: str, rpc_url: str) -> Optional[str]:
    """Wdraża program na Solana (solana-py, CLI). Zwraca adres programu lub None."""
    try:
        import subprocess
        # Wdrażanie przez CLI (solana program deploy ...)
        result = subprocess.run([
            "solana", "program", "deploy", program_path,
            "--keypair", keypair_path,
            "--url", rpc_url
        ], capture_output=True, text=True)
        if result.returncode == 0:
            # Parsowanie adresu programu z outputu
            for line in result.stdout.splitlines():
                if "Program Id:" in line:
                    return line.split(":")[1].strip()
        print(result.stdout)
        print(result.stderr)
        return None
    except Exception as e:
        print(f"Błąd wdrażania programu na Solana: {e}")
        return None
