import aiohttp, atexit, asyncio

session = aiohttp.ClientSession()


@atexit.register
def goodbye():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(session.close())


async def get_text_with_response_code(url):
    get_session = await session.get(url)
    text = await get_session.text()
    response = get_session.status
    return response, text


async def get_json_with_response_code(url):
    get_session = await session.get(url)
    json = await get_session.json()
    response = get_session.status
    return response, json


async def get_text(url):
    get_session = await session.get(url)
    text = await get_session.text()
    return text


async def get_json(url):
    get_session = await session.get(url)
    json_data = await get_session.json()
    return json_data


async def post_dictionary(url, data):
    post_session = await session.post(url, json=data)
    text = await post_session.text()
    response = post_session.status
    return response, text