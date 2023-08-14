from datetime import datetime, timezone
import sys
import requests
import json

class ApiConsume():
    session = requests.session()
    
    def __init__(self) -> None:
        pass

    def request(self, url, params = {}, headers = {}, method = 'get'):
    
        if (method == 'GET'):
            response = self.session.get(url, params=params, headers=headers)
        elif(method == 'POST'):
            response = self.session.post(url, params=params, headers=headers)
        
        content_str = ''

        if len(response.content) > 0:
            content_str = response.content.decode('utf-8')
        
        response.raise_for_status()

        if len(content_str) > 0:
            return json.loads(content_str)


        return response