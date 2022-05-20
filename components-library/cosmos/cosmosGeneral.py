import requests

class connect_to_cosmos:
    def __init__(self,link):
        self.link=link


    def get_latest_block(self):
        link=f'{self.link}/blocks/latest'
        request=requests.get(link)
        return request.json()