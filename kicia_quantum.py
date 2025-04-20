# kicia_quantum.py
"""
Moduł do obsługi połączeń z komputerami kwantowymi: IBM Quantum, Amazon Braket, Azure Quantum, D-Wave, IonQ, Rigetti.
Wymaga: qiskit, amazon-braket-sdk, azure-quantum, dwave-ocean-sdk, openqasm, itp.
"""
from typing import Optional
import os

def connect_ibm_quantum(api_token: str) -> bool:
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        QiskitRuntimeService.save_account(channel="ibm_quantum", token=api_token, overwrite=True)
        service = QiskitRuntimeService()
        print("Połączono z IBM Quantum!")
        return True
    except Exception as e:
        print(f"Błąd połączenia z IBM Quantum: {e}")
        return False

def connect_amazon_braket(aws_access_key: str, aws_secret_key: str, region: str = "us-west-2") -> bool:
    try:
        import boto3
        boto3.setup_default_session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)
        print("Połączono z Amazon Braket!")
        return True
    except Exception as e:
        print(f"Błąd połączenia z Amazon Braket: {e}")
        return False

def connect_azure_quantum(resource_id: str, location: str, credential=None) -> bool:
    try:
        from azure.quantum import Workspace
        ws = Workspace(resource_id=resource_id, location=location, credential=credential)
        print("Połączono z Azure Quantum!")
        return True
    except Exception as e:
        print(f"Błąd połączenia z Azure Quantum: {e}")
        return False

def connect_dwave(api_token: str) -> bool:
    try:
        from dwave.cloud import Client
        client = Client(token=api_token)
        print("Połączono z D-Wave Leap!")
        return True
    except Exception as e:
        print(f"Błąd połączenia z D-Wave: {e}")
        return False

def connect_ionq(api_token: str) -> bool:
    try:
        import requests
        # Testowe zapytanie do API IonQ
        headers = {"Authorization": f"apiKey {api_token}"}
        r = requests.get("https://api.ionq.co/v0/jobs", headers=headers)
        if r.status_code == 200:
            print("Połączono z IonQ Cloud!")
            return True
        else:
            print(f"Błąd połączenia z IonQ: {r.text}")
            return False
    except Exception as e:
        print(f"Błąd połączenia z IonQ: {e}")
        return False

def connect_rigetti(api_key: str, user_id: str) -> bool:
    try:
        import requests
        headers = {"Authorization": f"Token {api_key}"}
        r = requests.get(f"https://api.qcs.rigetti.com/v1/user/{user_id}", headers=headers)
        if r.status_code == 200:
            print("Połączono z Rigetti QCS!")
            return True
        else:
            print(f"Błąd połączenia z Rigetti: {r.text}")
            return False
    except Exception as e:
        print(f"Błąd połączenia z Rigetti: {e}")
        return False

def connect_all_quantum_services(credentials: dict) -> dict:
    """Łączy się ze wszystkimi obsługiwanymi komputerami kwantowymi. Zwraca słownik statusów."""
    status = {}
    status['ibm'] = connect_ibm_quantum(credentials.get('ibm_token', ''))
    status['amazon'] = connect_amazon_braket(credentials.get('aws_access_key', ''), credentials.get('aws_secret_key', ''))
    status['azure'] = connect_azure_quantum(credentials.get('azure_resource_id', ''), credentials.get('azure_location', ''))
    status['dwave'] = connect_dwave(credentials.get('dwave_token', ''))
    status['ionq'] = connect_ionq(credentials.get('ionq_token', ''))
    status['rigetti'] = connect_rigetti(credentials.get('rigetti_api_key', ''), credentials.get('rigetti_user_id', ''))
    return status
