import requests
import json

api_key = '3f5419954a54faf99fed'
secret_key = '0e228df580ce9b2762489db1cca3dd89cca53456259dd11fab64cf9d0f33ebfd'

def pin_to_ipfs(data):
    assert isinstance(data, dict), f"Error pin_to_ipfs expects a dictionary"
    pinata_url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers =  {
        "Content-Type": "application/json",
        "pinata_api_key": api_key,
        "pinata_secret_api_key": secret_key,
    }
    #json_data = json.dumps(data)
    post = requests.post(pinata_url, headers= headers, json=data)
    
    #Errors
    print("status:", post.status_code)
    print("text:", post.text)
    print("json:", post.json())
    return post.json()["IpfsHash"]

def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), f"get_from_ipfs accepts a cid in the form of a string"
    
    # Send a GET request to retrieve the data from IPFS
    pinata_url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    response = requests.get(pinata_url)
    
    return response.json()
    
if __name__ == "__main__":

    cid=pin_to_ipfs({'I saw' : 'water', "matban":"tancan"})
    print(cid)
    print(get_from_ipfs(cid))
