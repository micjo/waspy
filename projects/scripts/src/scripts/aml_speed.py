from typing import Tuple
import time
from datetime import datetime
import waspy.hardware_control.http_helper as http

url = "http://localhost:8000/api/aml_x_y"


def get_timestamp():
    my_date = datetime.now()
    return my_date.strftime('%Y.%m.%d__%H:%M__%S.%f')


def set_speed(x: Tuple[int, int, int], h: Tuple[int, int], m: Tuple[int, int, int], t: int):
    x_command = "X{},{},{}".format(x[0], x[1], x[2])
    http.post_request(url, {"send_command": x_command})
    h_command = "h{},{}".format(h[0], h[1])
    http.post_request(url, {"send_command": h_command})
    m_command = "M{},{},{}".format(m[0], m[1], m[2])
    http.post_request(url, {"send_command": m_command})
    t_command = "T{}".format(t)
    http.post_request(url, {"send_command": t_command})
    http.post_request(url, {"get_speed_settings": True})


def move_to_x_mm(position, debug_print=True):
    status = http.get_json(url)
    start_position = status["motor_1_position"]
    start = time.time()
    http.post_request(url, {"set_m1_target_position": position});
    end = time.time()
    if debug_print:
        print("Moving motor 1 from {} to {}, took {} msec".format(start_position, position, end - start))


def move_to_y_mm(position, debug_print=True):
    status = http.get_json(url)
    start_position = status["motor_2_position"]
    start = time.time()
    http.post_request(url, {"set_m2_target_position": position});
    end = time.time()
    if debug_print:
        print("Moving motor 2 from {} to {}, took {} msec".format(start_position, position, end - start))


def move_to_xy_mm(x_position, y_position, debug_print=True):
    move_to_x_mm(x_position, debug_print)
    move_to_y_mm(y_position, debug_print)


if __name__ == "__main__":
    print(http.get_json(url)["speed"])

    set_speed((75, 500, 1200), (49, 0), (160, 320, 600), 500)
    for i in range(0, 5):
        print(i)
        move_to_xy_mm(0, 0)
        move_to_xy_mm(1, 1)

    print(http.get_json(url)["speed"])
