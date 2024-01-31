import os
from web3 import Web3
from eth_typing import ChecksumAddress, HexAddress
import shortuuid
from dataclasses import dataclass
from eth_account import Account
import dotenv

dotenv.load_dotenv()


@dataclass
class PaymentInfo:
    id: str
    address: ChecksumAddress


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

private_key = os.getenv("OWNER_KEY")
account = Account.from_key(private_key)

provider = Web3(Web3.HTTPProvider("https://bsc-dataseed1.binance.org/"))

cur_path = os.path.abspath(__file__)
abi_path = file_path = os.path.join(os.path.dirname(cur_path), "abi.json")

contractAddress = provider.to_checksum_address(
    "0x057ef64e23666f000b34ae31332854acbd1c8544"
)
usdtAddress = provider.to_checksum_address(
    "0x261d8c5e9742e6f7f1076fa1f560894524e19cad",
)
treasuryAddress = provider.to_checksum_address(account.address)

with open(abi_path, "r") as f:
    abi = f.read()


contract = provider.eth.contract(address=contractAddress, abi=abi)
usdtContract = provider.eth.contract(address=usdtAddress, abi=balanceOfAbi)


def create_payment():
    payment_id = shortuuid.uuid()
    print("paymend id generated")
    adddress = contract.functions.getAddress(payment_id).call()
    return PaymentInfo(id=payment_id, address=adddress)


def check_usdt_balance(address: HexAddress):
    return usdtContract.functions.balanceOf(address).call()


def complete_payment(id: str, amount: int):
    amount = amount * 10**18

    trx_data = contract.functions.completePayment(
        id,
        amount,
        usdtAddress,
        treasuryAddress,
    )

    trx = trx_data.build_transaction(
        {
            "from": account.address,
            "nonce": provider.eth.get_transaction_count(account.address),
        }
    )
    signed_tx = account.sign_transaction(trx)

    tx_hash = provider.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = provider.eth.wait_for_transaction_receipt(tx_hash)
    status = receipt["status"]
    return status == 1
