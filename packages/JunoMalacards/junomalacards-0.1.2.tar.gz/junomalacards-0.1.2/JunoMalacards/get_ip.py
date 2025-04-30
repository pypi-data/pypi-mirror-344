import json

import requests

def get_ip(proxy_api:str):
    response = requests.get(proxy_api)
    response_json = response.text
    response_json = json.loads(response_json)
    proxy_list = [response_json["data"]["list"][0]["ip"], response_json["data"]["list"][0]["port"]]
    print(proxy_list)
    return proxy_list

if __name__ == "__main__":
    get_ip()

