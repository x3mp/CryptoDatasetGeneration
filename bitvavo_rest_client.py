import hashlib
import hmac
import json
import requests
import os
import python_bitvavo_api.bitvavo as bitvavo

from datetime import time
from dotenv import load_dotenv

load_dotenv()
APIKEY = os.getenv('APIKEY')
APISECRET = os.getenv('APISECRET')

bitvavo_api = bitvavo.Bitvavo({
    'APIKEY': APIKEY,
    'APISECRET': APISECRET
})

class BitvavoRestClient:
    def __init__(self, api_key: str, api_secret: str, bitvavo_api, access_window: int = 10000):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_window = access_window
        self.base = 'https://api.bitvavo.com/v2'

    def create_signature(self, timestamp: int, method: str, url: str, body: dict | None):
        string = str(timestamp) + method + '/v2' + url
        if (body is not None) and (len(body.keys()) != 0):
            string += json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.api_secret.encode('utf-8'), string.encode('utf-8'), hashlib.sha256).hexdigest()
        return signature

    def make_request(self, method, url, body=None):
        timestamp = int(time.time() * 1000)
        signature = self.create_signature(timestamp, method, url, body)
        headers = {
            'Bitvavo-Access-Key': self.api_key,
            'Bitvavo-Access-Signature': signature,
            'Bitvavo-Access-Timestamp': str(timestamp),
            'Bitvavo-Access-Window': str(self.access_window),
        }
        response = requests.request(method, self.base + url, headers=headers, json=body)
        return response.json()