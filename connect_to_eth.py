import json
from web3 import Web3
#from web3.middleware import geth_poa_middleware
from web3.middleware import ExtraDataToPOAMiddleware
from web3.providers.rpc import HTTPProvider

def connect_to_eth():
	url = "https://mainnet.infura.io/v3/2ea6510a3e0e4513b3d951b705f321a9"
	w3 = Web3(HTTPProvider(url))
	assert w3.is_connected(), f"Failed to connect to provider at {url}"
	return w3



def connect_with_middleware(contract_json):
	with open(contract_json, "r") as f:
		d = json.load(f)
		d = d['bsc']
		address = d['address']
		abi = d['abi']

	# TODO complete this method
	# The first section will be the same as "connect_to_eth()" but with a BNB url
	url = "https://bsc-mainnet.infura.io/v3/2ea6510a3e0e4513b3d951b705f321a9"
	w3 = Web3(HTTPProvider(url))
	assert w3.is_connected(), f"Failed to connect to provider at {url}"

	# The second section requires you to inject middleware into your w3 object and
	# create a contract object. Read more on the docs pages at https://web3py.readthedocs.io/en/stable/middleware.html
	# and https://web3py.readthedocs.io/en/stable/web3.contract.html
  	
	w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

	contract = w3.eth.contract(abi=abi, address=address)
	return w3, contract

if __name__ == "__main__":

	# w3 = connect_to_eth()
	# print("Connected:", w3.is_connected())
	# print(w3.eth.block_number)

	w3, contract = connect_with_middleware('contract_info.json')
	
	print("Connected:", w3.is_connected())
	print("Chain ID:", w3.eth.chain_id)
	print("Latest block:", w3.eth.block_number)
	print("Contract address:", contract.address)