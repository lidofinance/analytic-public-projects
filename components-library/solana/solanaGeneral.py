import requests

class connect_to_solana:
    def __init__(self,link):
        self.link=link

    def get_latest_block(self):
        headers = {'Content-type': 'application/json'}
        data = '{"id":1,"jsonrpc":"2.0","method":"getLatestBlockhash","params":[{"commitment":"confirmed"}]}'
        response = requests.post(self.link, headers=headers, data=data)
        return response.json()['result']['context']['slot']

    '''def get_latest_block(self):
        headers = {'Content-type': 'application/json'}
        last_block= self.get_latest_block_slot()-1
        data = '{"jsonrpc": "2.0","id":1,"method":"getBlock","params":['+str(last_block)+',{"commitment":"confirmed"}]}'
        response = requests.post(self.link, headers=headers, data=data)
        return response.json()'''

