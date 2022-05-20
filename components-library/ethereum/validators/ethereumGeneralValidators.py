import requests
import ethereum.ethereumGeneral as eth

class eth_validator(eth.connect_to_ethereum):
    def __init__(self,link):
        super().__init__(link)

    def get_validator_info_by_index(self,index):
        link = f'https://www.rated.network/api/v0/validators/{index}/effectiveness?&size=539'
        responce = requests.get(link)
        return responce.json()