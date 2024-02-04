import os
from web3 import Web3
from web3.middleware.geth_poa import geth_poa_middleware
from eth_typing import ChecksumAddress, HexAddress
import shortuuid
from dataclasses import dataclass
from eth_account import Account
import dotenv

dotenv.load_dotenv()

testing = False


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
provider.middleware_onion.inject(geth_poa_middleware, layer=0)
cur_path = os.path.abspath(__file__)
abi_path = file_path = os.path.join(os.path.dirname(cur_path), "abi.json")

contractAddress = provider.to_checksum_address(
    "0x64c5ad4fd804a66f9acfe4f525990d6637e1ba94"
)
usdtAddress = provider.to_checksum_address(
    "0x55d398326f99059fF775485246999027B3197955",
)
treasuryAddress = provider.to_checksum_address(
    "0x65deA9dbf212c5232E377a56E4D5273c0533F24b"
)

with open(abi_path, "r") as f:
    abi = f.read()


contract = provider.eth.contract(address=contractAddress, abi=abi)
usdtContract = provider.eth.contract(address=usdtAddress, abi=balanceOfAbi)


def create_payment():
    payment_id = shortuuid.uuid()
    print("paymend id generated")
    if testing:
        address = Account.create().address
    else:
        address = contract.functions.getAddress(payment_id).call()
    return PaymentInfo(id=payment_id, address=address)


def check_usdt_balance(address: HexAddress, balance: int = 100):
    if testing:
        return balance
    else:
        return usdtContract.functions.balanceOf(address).call()


def complete_payment(id: str, amount: int, to=treasuryAddress):
    if testing:
        return True

    amount = amount * 10**18

    trx_data = contract.functions.completePayment(
        id,
        amount,
        usdtAddress,
        to,
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
