import tornado.httpclient
import tornado.escape
import json

session = tornado.httpclient.AsyncHTTPClient()


async def get_text_with_response_code(url):
    http_request = tornado.httpclient.HTTPRequest(url=url, connect_timeout=2.0, request_timeout=5.0)
    http_response = await session.fetch(http_request, raise_error=False)
    text = tornado.escape.to_unicode(http_response.body)
    return http_response.code, text


async def get_json_with_response_code(url):
    http_request = tornado.httpclient.HTTPRequest(url=url, connect_timeout=2.0, request_timeout=5.0)
    http_response = await session.fetch(http_request, raise_error=False)
    json_data = tornado.escape.json_decode(http_response.body)
    return http_response.code, json_data


async def get_text(url):
    http_request = tornado.httpclient.HTTPRequest(url=url, connect_timeout=2.0, request_timeout=5.0)
    http_response = await session.fetch(http_request)
    text = tornado.escape.to_unicode(http_response.body)
    return text


async def get_json(url):
    http_request = tornado.httpclient.HTTPRequest(url=url, connect_timeout=2.0, request_timeout=5.0)
    http_response = await session.fetch(http_request)
    json_data = tornado.escape.json_decode(http_response.body)
    return json_data


async def post_dictionary(url, data):
    body = json.dumps(data)
    http_request = tornado.httpclient.HTTPRequest(url=url, connect_timeout=2.0, request_timeout=5.0, method='POST',
                                                  body=body)
    http_response = await session.fetch(http_request, raise_error=False)
    return http_response.code, http_response.body
