import tornado.httpclient
import tornado.escape
import json

session = tornado.httpclient.AsyncHTTPClient()


async def get_text_with_response_code(url):
    http_response = await session.fetch(url)
    text = tornado.escape.to_unicode(http_response.body)
    return http_response.code, text


async def get_json_with_response_code(url):
    http_response = await session.fetch(url)
    json_data = tornado.escape.json_decode(http_response.body)
    return http_response.code, json_data


async def get_text(url):
    http_response = await session.fetch(url)
    text = tornado.escape.to_unicode(http_response.body)
    return text


async def get_json(url):
    http_response = await session.fetch(url)
    json_data = tornado.escape.json_decode(http_response.body)
    return json_data


async def post_dictionary(url, data):
    body = json.dumps(data)
    http_response = await session.fetch(url, method='POST', body=body)
    return http_response
