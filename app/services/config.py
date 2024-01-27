import os
from web3 import Web3

balanceOfAbi = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    }
]


provider = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
cur_path = os.path.abspath(__file__)
abi_path = file_path = os.path.join(os.path.dirname(cur_path), "abi.json")

contractAddress = provider.to_checksum_address(
    "0x48df654a5431182e6d386a10dbdda5c58d4dddc2"
)
usdtAddress = provider.to_checksum_address(
    "0x018ecbad742fa1ce05efd0981f36eb14d9625e14",
)


with open(abi_path, "r") as f:
    contractAbi = f.read()

contract = provider.eth.contract(address=contractAddress, abi=contractAbi)
usdtContract = provider.eth.contract(address=usdtAddress, abi=balanceOfAbi)


__all__ = [
    "contract",
    "usdtAddress",
    "provider",
    "usdtContract",
]
