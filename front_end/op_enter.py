from web3 import Web3, HTTPProvider
import solcx
from typing import Dict, Union, Any
from contract import deploy_contract, interact_contract
import json

web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

def interactWithContract(compiled_contract_path: str, contract_name: str, proof_path: str):
    #interact with contract
    with open(compiled_contract_path, 'r') as f:
        contract_info = json.load(f)
        contract_address = contract_info[contract_name + '_address']
        compiled_contract_abi = contract_info['abi']
    contract = web3.eth.contract(address=contract_address, abi=compiled_contract_abi)
    # get proof and input
    with open(proof_path, 'r') as f:
        proof = f.read()
    a = [int(proof[2:68], 16), int(proof[72:138], 16)]
    b = [[int(proof[144:210], 16), int(proof[214:280], 16)], [int(proof[285:351], 16), int(proof[355:421], 16)]]
    c = [int(proof[427:493], 16), int(proof[497:563], 16)]
    input_ = [int(proof[568:634], 16), int(proof[637:703], 16)]
    # call the deposit function of mixer
    contract_call = contract.functions.deposit(a,b,c,input_)
    sender_eth_address = web3.eth.accounts[1]
    sender_eth_private_key = '7df411fbf0bfc622fa52b8f78c197471c7b6765e8c0642492d403341aff8ad22'
    value = 1
    gas = 3000000
    (tx_receipt, transaction_contract_ouput) = interact_contract(web3, contract_call, sender_eth_address, sender_eth_private_key, value, gas)
    print(transaction_contract_ouput)

if __name__ == "__main__":
    # web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
    # contract_source_path = 'E:/BlockChain/program/contracts/StoreVar.sol'
    # contract_name = 'StoreVar'
    # contract_source_path = 'E:/mixer/back_end/contracts/MyMiMC.sol'
    # contract_name = 'MyMiMC' #0x88b4A72e29749D1CdB611582ADE02A662C3E7ff9
    # contract_source_path = 'E:/mixer/back_end/contracts/MerkleTree_MiMC.sol'
    # contract_name = 'MerkleTree_MiMC' #0x301Dd529363dD54A38861D05Fd706e075aBDB415
    # contract_source_path = 'E:/mixer/back_end/contracts/VerifyDeposit.sol'
    # contract_name = 'Verifier' #0x4795f0621abA182A2c14E780B0a4Dab2F67cACda
    # contract_source_path = 'E:/mixer/back_end/contracts/Mixer.sol'
    # contract_name = 'Mixer'  
    # deployContract(contract_source_path, contract_name)  

    contract_name = 'Mixer'
    compiled_contract_path = 'E:/mixer/back_end/compiled_contracts/compiled_' + contract_name + '_info.txt'
    proof_path = 'E:/mixer/front_end/zksnarks_proof/depositproof.txt'
    interactWithContract(compiled_contract_path, contract_name, proof_path)
