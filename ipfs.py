import json
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from web3.providers.rpc import HTTPProvider

'''If you use one of the suggested infrastructure providers, the url will be of the form
now_url  = f"https://eth.nownodes.io/{now_token}"
alchemy_url = f"https://eth-mainnet.alchemyapi.io/v2/{alchemy_token}"
infura_url = f"https://mainnet.infura.io/v3/{infura_token}"
'''

import requests
import json

def pin_to_ipfs(data):
    assert isinstance(data, dict), f"Error pin_to_ipfs expects a dictionary"
    json_data = json.dumps(data)
    post = requests.post("http://127.0.0.1:5001/api/v0/add", files={"file": json_data})

    if post.status_code == 200:
        cid = post.json().get("Hash")
        return cid

def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), f"get_from_ipfs accepts a cid in the form of a string"
    
    # Send a GET request to retrieve the data from IPFS
    response = requests.post("http://127.0.0.1:5001/api/v0/cat", params={"arg": cid})

    
    if response.status_code == 200:
        # Parse the response content based on the expected content type
        if content_type == "json":
            data = json.loads(response.text)
        else:
            data = response.text  # Return as text if not JSON
            
        assert isinstance(data, dict), f"get_from_ipfs should return a dict"
        return data
    else:
        raise Exception(f"Error fetching data from IPFS: {response.text}")