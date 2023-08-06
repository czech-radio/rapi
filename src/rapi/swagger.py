import json
import logging
import os
import sys

import requests
import yaml

from rapi.logger import log_stderr as loge
from rapi.logger import log_stdout as logo

# import openapi3_parser
# from swagger_parser import SwaggerParser
# from openapi_parser import parse as swparse


# def swagger_download(url: str):
### urls:
#### https://rapidoc.croapp.cz/index.html ->
#### url="https://rapidoc.croapp.cz/apifile/openapi.yaml"
### save swagger definition file
# swagger_file = "./runtime/rapidev_croapp.yml"
# try:
# with open(swagger_file, "w", encoding="utf8") as file:
# file.write(r.text)
# except IOError as err:
# loge.error(f"error saving the file:{err}")


# data = yaml.safe_load(response.content)
# ystr=yaml.dump(data,allow_unicode=True)
# swagger_orig_file="swagger_orig.yaml"
# with open(swagger_orig_file, "w",encoding='utf8') as file:
# file.write(ystr)
# print(response.content)
# data = yaml.safe_load(response.content)
# parser=SwaggerParser(response.content)
# parser=SwaggerParser(url)
# print(dir(openapi_parser))
# print(openapi_parser.__builtins__)
# print(openapi_parser.version_info)
# print(openapi_parser.__pdoc__)

# if response.status_code == 200:
# with open(filename, "wb") as file:
# file.write(response.content)
# print("Failed to download the file. Status code:", response.status_code)


# url="https://rapidev.croapp.cz/stations?page[1]=0&page[limit]=1"
# headers = {"Authorization": "Bearer your_token"}
# params = {"param1": "value1", "param2": "value2"}
# headers = {}
# params = {}
# response = requests.get(url, headers=headers, params=params)
# print(response.json())
