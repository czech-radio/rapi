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


def swagger_download(url: str):
    ### urls:
    #### https://rapidoc.croapp.cz/index.html ->
    #### url="https://rapidoc.croapp.cz/apifile/openapi.yaml"
    try:
        ### download url
        r = requests.get(url)
    except requests.exceptions.HTTPError as errh:
        loge.error(errh)
        sys.exit(0)
    except requests.exceptions.ConnectionError as errc:
        loge.error(f"Connection Error: {errc}")
        sys.exit(0)
    except requests.exceptions.Timeout as errt:
        loge.error(f"Timeout Error:{errt}")
        sys.exit(0)
    except requests.exceptions.RequestException as err:
        loge.error(f"unknow exception:{err}")
        sys.exit(0)
    ### save swagger definition file
    swagger_file = "./runtime/rapidev_croapp.yml"
    try:
        with open(swagger_file, "w", encoding="utf8") as file:
            file.write(r.text)
    except IOError as err:
        loge.error(f"error saving the file:{err}")


# def swagger_parse(swagger_file: str):
# parser = swparse(swagger_file)
# pass
# content = swparse(swagger_file)
# parser=SwaggerParser(swagger_file)

# data = yaml.safe_load(response.content)
# ystr=yaml.dump(data,allow_unicode=True)
# print(data)
# print(ystr)
# swagger_orig_file="swagger_orig.yaml"
# with open(swagger_orig_file, "w",encoding='utf8') as file:
# file.write(ystr)
# print(response)
# print("hell")
# print(response.content)
# data = yaml.safe_load(response.content)
# print(data)
# parser=SwaggerParser(response.content)
# parser=SwaggerParser(url)
# print(dir(openapi_parser))
# print(openapi_parser.__builtins__)
# print(openapi_parser.version_info)
# print(openapi_parser.__pdoc__)
# content=openapi_parser.parse(data)
# content=parse(data)
# content = parse('swagger.yml')
# print(content)

# print(data)
# if response.status_code == 200:
# with open(filename, "wb") as file:
# file.write(response.content)
# print("File downloaded successfully.")
# else:
# print("Failed to download the file. Status code:", response.status_code)


# DownloadApiDefinition()

# url="https://rapidev.croapp.cz/stations?page[1]=0&page[limit]=1"
# headers = {"Authorization": "Bearer your_token"}
# params = {"param1": "value1", "param2": "value2"}
# headers = {}
# params = {}
# response = requests.get(url, headers=headers, params=params)
# print(response.json())

# class station:
# def item_generator(json_input, lookup_key):
# if isinstance(json_input, dict):
# for k, v in json_input.items():
# if k == lookup_key:
# yield v
# else:
# yield from item_generator(v, lookup_key)
# elif isinstance(json_input, list):
# for item in json_input:
# yield from item_generator(item, lookup_key)
