import http.client
import os
import requests
import json


response = requests.post("https://graphql.jino.ru/user/", json=data, headers=headers)
print(response.status_code, response.text)
