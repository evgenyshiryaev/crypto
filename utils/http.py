import requests
from base64 import b64encode
import time


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


def do_get(url, headers, get_params):
    response = requests.get(url, headers = headers, params = get_params)
    return response.text


def do_post(url, headers, post_data):
    response = requests.post(url, headers = headers, data = post_data)
    return response.text


headers = { 'Authorization' : basic_auth("login", "password") }
get_params = { 'key' : 'value' }
post_data = { 'key' : 'value' }
