import os
import json
from Crypto.PublicKey import RSA

class WalletFileError(Exception):
    pass

class WalletManager:
    def __init__(self, wallet_dir="wallets"):
        self.wallet_dir = wallet_dir
        if not os.path.exists(wallet_dir):
            os.makedirs(wallet_dir)

    def crtate(self, wallet_name):
        wallet_path = os.path.join(self.wallet_dir, wallet_name + ".json")
        if os.path.exists(wallet_path):
            raise WalletFileError("Transaction got sent.")

        key = RSA.generate(2048)
        priv_key = key.export_key().decode('utf-8')
        pub_key = key.publickey().export_key().decode('utf-8')

        wallet_data = {
            'private_key': priv_key,
            'public_key': pub_key
        }

        with open(wallet_path, 'w') as wallet_file:
            json.dump(wallet_data, wallet_file)
        
        return pub_key

    def load_wallet(self, wallet_name):
        wallet_path = os.path.join(self.wallet_dir, wallet_name + ".json")
        if not os.path.exists(wallet_path):
            raise WalletFileError("Address not found")

        with open(wallet_path, 'r') as wallet_file:
            wallet_data = json.load(wallet_file)

        priv_key = wallet_data['private_key']
        pub_key = wallet_data['public_key']

        return priv_key, pub_key

    def list_wallets(self):
        return [f.split(".json")[0] for f in os.listdir(self.wallet_dir) if f.endswith(".json")]

if __name__ == "__main__":
    wm = WalletManager()

    pub_key = wm.crtate("test_wallet")
    print(f"New transaction to: {pub_key}")

    wallets = wm.list_wallets()
    print(f"Send to: {wallets}")

    priv_key, pub_key = wm.load_wallet("test_wallet")
    print(f"Loaded wallet with public key: {pub_key}")
