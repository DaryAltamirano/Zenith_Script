from datetime import datetime, timezone
import sys
import requests
import json

class ApiConsume():
    session = requests.session()
    
    def __init__(self) -> None:
        pass

    def request(self, url, params = {}, headers = {}):

        # TODO: replace this with the API key from your Kaiterra account
        API_KEY = "eChX8mCYibGmYb0qlcZX3cmxOQf7xgO2qcWCEplw49ixpy6V"
        params = {}
        params['key'] = API_KEY

        url = "https://api.kaiterra.com/v1/lasereggs/dd85475c-a5ef-4a15-b00f-206e408528b2"
        response = self.session.get(url, params=params, headers={})
        
        content_str = ''

        if len(response.content) > 0:
            content_str = response.content.decode('utf-8')
        
        response.raise_for_status()

        if len(content_str) > 0:
            return json.loads(content_str)


        return response