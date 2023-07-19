from datetime import datetime, timezone
import sys
import requests
import json

class ApiConsume():
    session = requests.session()
    
    def __init__(self) -> None:
        pass

    def request(self, url, params = {}, headers = {}):

        response = self.session.get(url, params=params, headers=headers)
        
        content_str = ''

        if len(response.content) > 0:
            content_str = response.content.decode('utf-8')
        
        response.raise_for_status()

        if len(content_str) > 0:
            return json.loads(content_str)


        return response