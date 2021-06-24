import asyncio
import app.hardware_controllers.daemon_comm as comm
import app.hardware_controllers.http_helper as http
from typing import Tuple
import time
from datetime import datetime

url = "http://localhost:5000/api/aml_x_y"


def get_timestamp():
    my_date = datetime.now()
    return my_date.strftime('%Y.%m.%d__%H:%M__%S.%f')


async def set_speed_and_print(x: Tuple[int, int, int], h: Tuple[int, int], m: Tuple[int, int, int], t: int):
    x_command = "X{},{},{}".format(x[0], x[1], x[2])
    await comm.post_request(url, {"request_id": "set_x", "send_command": x_command})
    h_command = "h{},{}".format(h[0], h[1])
    await comm.post_request(url, {"request_id": "set_h", "send_command": h_command})
    m_command = "M{},{},{}".format(m[0], m[1], m[2])
    await comm.post_request(url, {"request_id": "set_m", "send_command": m_command})
    t_command = "T{}".format(t)
    await comm.post_request(url, {"request_id": "set_t", "send_command": t_command})
    await comm.post_request(url, {"request_id": "get_speed", "get_speed_settings": True})
    status = await http.get_json(url)
    print(status["speed"])


async def move_to_x_mm(position, debug_print=True):
    status = await http.get_json(url)
    start_position = status["motor_1_position"]
    start = time.time()
    await comm.post_request(url, {"request_id": get_timestamp(), "set_m1_target_position": position});
    end = time.time()
    if debug_print:
        print("Moving motor 1 from {} to {}, took {} msec".format(start_position, position, end - start))


async def move_to_y_mm(position, debug_print=True):
    status = await http.get_json(url)
    start_position = status["motor_2_position"]
    start = time.time()
    await comm.post_request(url, {"request_id": get_timestamp(), "set_m2_target_position": position});
    end = time.time()
    if debug_print:
        print("Moving motor 2 from {} to {}, took {} msec".format(start_position, position, end - start))


async def move_to_xy_mm(x_position, y_position, debug_print=True):
    await move_to_x_mm(x_position, debug_print)
    await move_to_y_mm(y_position, debug_print)


async def main():
    status = await http.get_json(url)
    print(status["speed"])
    await set_speed_and_print((75, 500, 1200), (49, 0), (160, 320, 600), 500)
    for i in range(0,5):
        await move_to_xy_mm(70, 55)
        await move_to_xy_mm(80, 60)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
