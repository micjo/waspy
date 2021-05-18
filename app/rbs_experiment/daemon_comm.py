import aiohttp
import asyncio
import logging

session = aiohttp.ClientSession()

async def wait_for_request_done(url, request):
    while True:
        await asyncio.sleep(0.2)
        getSession = await session.get(url)
        response = await getSession.json()
        error_message = response["error"]
        if (error_message == "Success" or error_message == "No Error"):
            if (response['request_finished'] and response["request_id"] == request["request_id"]):
                break
        else:
            raise Exception(url + ": " + error_message)


async def post_request(url, request):
    logging.info("post to: " +url + ", content: " + str(request))
    await session.post(url, json=request)
    await wait_for_request_done(url, request)

async def get_json_status(url):
    getSession = await session.get(url)
    response = await getSession.json()
    return response

async def set_motrona_target_charge(request_id, url, target_charge):
    motrona_request = {}
    motrona_request["request_id"] = request_id
    motrona_request["target_charge"] = target_charge
    await post_request(url, motrona_request)

async def move_aml_first(request_id, url, position):
    aml_request = {}
    aml_request["request_id"] = request_id
    aml_request["set_m1_target_position"] = position
    await post_request(url, aml_request)

async def move_aml_second(request_id, url, position):
    aml_request = {}
    aml_request["request_id"] = request_id
    aml_request["set_m2_target_position"] = position
    await post_request(url, aml_request)

async def move_aml_both(request_id, url, positions):
    aml_request = {}
    aml_request["request_id"] = request_id
    aml_request["set_m1_target_position"] = positions[0]
    aml_request["set_m2_target_position"] = positions[1]
    await post_request(url, aml_request)

async def clear_start_motrona_count(request_id, url):
    motrona_request = {}
    motrona_request["request_id"] = request_id
    motrona_request["clear-start_counting"] = True
    await post_request(url, motrona_request)

async def pause_motrona_count(request_id, url):
    motrona_request = {}
    motrona_request["request_id"] = request_id
    motrona_request["pause_counting"] = True
    await post_request(url, motrona_request)

async def motrona_counting_done(url):
    while True:
        await asyncio.sleep(1)
        response = await get_json_status(url)
        if (response["status"] == "Done"):
            logging.info("motrona counting done")
            break

async def clear_and_arm_caen_acquisition(request_id, url):
    request = {}
    request['request_id'] = request_id
    request['clear_acquisition'] = True
    request['start_acquisition'] = True
    await post_request(url, request)

