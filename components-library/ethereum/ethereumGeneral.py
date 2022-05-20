from web3 import Web3

class connect_to_ethereum:
    def __init__(self,link):
        self.link=link
        self.connection=Web3(Web3.HTTPProvider(self.link))

    def get_latest_block(self):
        return self.connection.eth.get_block('latest')
