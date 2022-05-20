import requests
import ethereum.ethereumGeneral as eth

class eth_token(eth.connect_to_ethereum):
    def __init__(self,link):
        super().__init__(link)

    def get_token_holders(self,token_address):
        link = f'https://api.ethplorer.io/getTopTokenHolders/{token_address}?apiKey=freekey&limit=100'
        request = requests.get(link)
        return request.json()

    def check_if_contract(self,address):
        proper_address = self.connetion.toChecksumAddress(address)
        code = self.connection.eth.get_code(proper_address)
        if str(code) == "b''":
            return 'private_address'
        return 'contract'

    def get_contract_holders(self,token_address):
        '''Return list of contracts, which hold token, contracts are taken from top 100 holders
        reqires funtion check_if_contract() for proper work'''
        contract_holders = []
        holders = self.get_token_holders(token_address)
        for x in range(len(holders['holders'])):
            address_type = self.check_if_contract(holders['holders'][x]['address'])
            if address_type == 'contract':
                contract_holders.append(holders['holders'][x])
        return contract_holders