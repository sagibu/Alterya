import requests
import uvicorn
from fastapi import FastAPI

# from requests.auth import HTTPBasicAuth


# # print(certifi.where())


API_KEY = "cqt_rQw7bmthQ8q33gWyPmGwF8jWyTBT"
WALLET_ADDRESS = "0x6105f0b07341eE41562fd359Ff705a8698Dd3109"
CHAIN = "eth-mainnet"


class API:
    def make_request(self, url, params = '',headers = {
    'Content-Type': 'application/json',
    }):
        response = requests.get(
            url,
            params=params,
            headers=headers,
            auth=('cqt_wFy8xh6DWW4kKmDmBY8MjTKkFPBD', ''),
        )

        return response.json()


    def get_balances_response(self, wallet_address, chain_id):
        url = f"https://api.covalenthq.com/v1/{chain_id}/address/{wallet_address}/balances_v2/"
        
        return self.make_request(url)


    def get_assets(self, wallet_address, chain_id):
        response = self.get_balances_response(wallet_address, chain_id)

        assets = [item["contract_name"] for item in response["data"]["items"] if item["quote"]]
        return assets

    def get_balances(self, wallet_address, chain_id):
        response = self.get_balances_response(wallet_address, chain_id)

        return sum([item["quote"] for item in response["data"]["items"] if item["quote"]])


    def get_paginated_transactions(self, wallet_address, page, chain_id):
        url = f"https://api.covalenthq.com/v1/{chain_id}/address/{wallet_address}/transactions_v3/page/{page}/"
        return self.make_request(url)




# print(get_assets())

# import requests
# headers = {
#  'Content-Type': 'application/json',
# }
# url = f"https://api.covalenthq.com/v1/{CHAIN}/address/{WALLET_ADDRESS}/balances_v2/"
# params = ''
# response = requests.get(
#     'https://api.covalenthq.com/v1/eth-mainnet/address/0x6105f0b07341eE41562fd359Ff705a8698Dd3109/balances_v2/',
#  params=params,
#  headers=headers,
#  auth=('cqt_wFy8xh6DWW4kKmDmBY8MjTKkFPBD', ''),
# )

# print(response.text)

app = FastAPI()

api = API()


@app.get("/{wallet_address}/assets/{chain_id}")
async def assets(wallet_address, chain_id):
    return api.get_assets(wallet_address, chain_id)

@app.get("/{wallet_address}/balance/{chain_id}")
async def balance(wallet_address, chain_id):
    return api.get_balances(wallet_address, chain_id)

@app.get("/{wallet_address}/transactions/{chain_id}")
async def transactions(wallet_address, page, chain_id):
    return api.get_paginated_transactions(wallet_address, page, chain_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)