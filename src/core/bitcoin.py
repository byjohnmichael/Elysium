from bitcoinlib.wallets import Wallet
from bitcoinlib.mnemonic import Mnemonic

current_network = "testnet"
current_witness_type = "segwit"

def gen_seed(): return Mnemonic().generate()

def create_wallet(wallet_name, seed=None):
    if seed == None:
        seed = Mnemonic().generate()
    raw_seed = Mnemonic().to_seed(seed)
    wallet = Wallet.create(wallet_name,
                           seed=raw_seed,
                           network=current_network,
                           witness_type=current_witness_type
    )
