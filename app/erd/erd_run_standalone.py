from app.erd.entities import ErdHardware, ErdRqm
from app.erd.erd_hardware import ErdSetup

if __name__ == "__main__":
    erd_hardware = ErdHardware.parse_obj({
        "mdrive_z": {"type": "mdrive", "title": "mpa3", "url": "http://localhost:22400/api/latest",
                     "proxy": "mdrive_z"},
        "mdrive_theta": {"type": "mdrive", "title": "mpa3", "url": "http://localhost:22401/api/latest",
                         "proxy": "mdrive_theta"},
        "mpa3": {"type": "mpa3", "title": "mpa3", "url": "http://localhost:22500/api/latest",
                 "proxy": "mpa3"}
    })

    erd = ErdSetup(erd_hardware)

    erd_rqm = ErdRqm.parse_obj({
        "recipes": [
            {"measuring_time_sec": 30, "spectrum_filename": "test_001", "theta": 10, "z_min": 0, "z_max": 30,
             "z_step": 2},
            {"measuring_time_sec": 30, "spectrum_filename": "test_002", "theta": 10, "z_min": 0, "z_max": 30,
             "z_step": 2},
        ]
    })
