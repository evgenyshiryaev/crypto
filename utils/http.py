import base64
import requests


def basic_auth(username, password):
    token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


def do_get(url, headers, get_params):
    response = requests.get(url, headers=headers, params=get_params)
    return response.text


def do_post(url, headers, post_data):
    response = requests.post(url, headers=headers, data=post_data)
    return response.text


_headers = {'Authorization': basic_auth("login", "password")}
_get_params = {'key': 'value'}
_post_data = {'key': 'value'}
