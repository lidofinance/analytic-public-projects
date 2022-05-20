from web3 import Web3
import requests

class connect_to_polygon:
    def __init__(self,link):
        self.link=link


    def get_latest_block(self):
        headers = {'Content-type': 'application/json'}
        data = '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
        response = requests.post(self.link, headers=headers, data=data)
        return response.json()
