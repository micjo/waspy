import requests


def get_text_with_response_code(url):
    response = requests.get(url)
    return response.status_code, response.text


def get_json_with_response_code(url):
    response = requests.get(url)
    return response.status_code, response.json()


def get_text(url):
    response = requests.get(url)
    return response.text


def get_json(url):
    return requests.get(url).json()


def post_dictionary(url, data):
    response = requests.post(url, json=data)
    return response.status_code, response.text
