import ethereum.ethereumGeneral as eth

class eth_contract(eth.connect_to_ethereum):
    def __init__(self,link,address,abi):
        super().__init__(link)
        self.address = address
        self.abi=abi



