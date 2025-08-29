import time

import logging
from threading import Lock

from waspy.drivers.fastcom_mpa3 import FastcomMpa3
from waspy.drivers.ims_mdrive import ImsMDrive
from waspy.drivers.motrona_dx350 import MotronaDx350
from waspy.iba.erd_entities import ErdDriverUrls, PositionCoordinates, ErdData
from waspy.iba.preempt import preemptive
from pathlib import Path
import numpy as np

class ErdSetup:
    _fake: bool
    _fake_count: int
    _cancel: bool

    def __init__(self, erd_driver_urls: ErdDriverUrls, param_folder: Path, tof_chmin: int, tof_chmax: int):
        self.mdrive_z = ImsMDrive(erd_driver_urls.mdrive_z)
        self.mdrive_theta = ImsMDrive(erd_driver_urls.mdrive_theta)
        self.mpa3 = FastcomMpa3(erd_driver_urls.mpa3)
        self.motrona_z_encoder = MotronaDx350(erd_driver_urls.motrona_z_encoder)
        self.motrona_theta_encoder = MotronaDx350(erd_driver_urls.motrona_theta_encoder)
        self._param_folder = param_folder
        self._lock = Lock()
        self._abort = False
        self._fake = False
        self._fake_count = 0
        self._cancel = False
        self._BPARAMS_FILE = "Bparams.txt"
        self._TOF_FILE = "Tof.in"
        self._tof_chmin = tof_chmin
        self._tof_chmax = tof_chmax

    def get_b_param_file_path(self) -> Path:
        return self._param_folder / self._BPARAMS_FILE
    
    def get_tof_file_path(self) -> Path:
        return self._param_folder / self._TOF_FILE
    
    def _get_tof_chmin_chmax(self) -> tuple[int, int]:
        return self._tof_chmin, self._tof_chmax
    
    def convert_to_extended_flt_data(self, histogram: str):
        np_histogram = _load_flt_data(histogram)
        # nanoseconds ? time_offset ? to be figured out
        ns_channel, t_offset = _load_tof_calibration(self.get_tof_file_path())
        b0,b1,b2 = _load_bparams_calibration(self.get_b_param_file_path(), self._tof_chmin, self._tof_chmax)
        return _extend_flt_data(np_histogram, b0, b1, b2, ns_channel, t_offset)


    def do_params_exist(self):
        return (self.get_b_param_file_path()).is_file() and (self.get_tof_file_path()).is_file()

    def cancel(self):
        self._cancel = True

    def resume(self):
        if not self._fake:
            self._cancel = False

    def fake(self):
        self._fake = True

    @preemptive
    def move(self, position: PositionCoordinates):
        if position is None:
            return
        logging.info("[WASPY.IBA.ERD_SETUP] moving erd system to '" + str(position) + "'")
        self.mdrive_z.move(position.z)
        self.mdrive_theta.move(position.theta)

    @preemptive
    def load(self):
        self.mdrive_z.load()
        self.mdrive_theta.load()

    def get_status(self, get_histogram=False) -> ErdData:
        status_mdrive_z = self.mdrive_z.get_status()
        status_mdrive_theta = self.mdrive_theta.get_status()
        status_mpa3 = self.mpa3.get_status()
        status_motrona_z_encoder = self.motrona_z_encoder.get_status()
        status_motrona_theta_encoder = self.motrona_theta_encoder.get_status()

        histogram = ""
        if get_histogram:
            histogram = self.get_histogram()
        return ErdData.parse_obj(
            {"mdrive_z": status_mdrive_z, "mdrive_theta": status_mdrive_theta, "mpa3": status_mpa3,
             "motrona_z_encoder": status_motrona_z_encoder,
             "motrona_theta_encoder": status_motrona_theta_encoder,
             "histogram": histogram, "measuring_time_sec": self.get_measuring_time()})

    @preemptive
    def wait_for_arrival(self):
        self.mdrive_theta.wait_for_move_done()
        self.mdrive_z.wait_for_move_done()
        logging.info("[WASPY.IBA.ERD_SETUP] Motors have arrived")

    @preemptive
    def wait_for(self, seconds):
        sleep_time = 0
        while sleep_time < seconds:
            yield
            time.sleep(1)
            sleep_time += 1

    @preemptive
    def wait_for_acquisition_done(self):
        logging.info("[WASPY.IBA.ERD_SETUP] Wait for acquisition completed")
        self._acquisition_done()
        logging.info("[WASPY.IBA.ERD_SETUP] Acquisition completed")

    @preemptive
    def wait_for_acquisition_started(self):
        self._acquisition_started()
        logging.info("[WASPY.IBA.ERD_SETUP] Acquisition Started")

    def get_histogram(self):
        if self._cancel:
            return ""
        if self._fake:
            logging.warn("[WASPY.IBA.ERD_SETUP] Returning fake data for histogram")
            with open(self._param_folder / "ERD25_090_01A.flt", 'r') as f:
                return f.read()
        return self.mpa3.get_histogram()

    @preemptive
    def configure_acquisition(self, measuring_time_sec: int, spectrum_filename: str):
        self.mpa3.stop_and_clear()
        self.mpa3.configure(measuring_time_sec, spectrum_filename)

    @preemptive
    def reupload_cnf(self):
        self.mpa3.reupload_mpa3_cnf()

    def initialize(self):
        self.reupload_cnf()

    @preemptive
    def start_acquisition(self):
        self.mpa3.start()

    @preemptive
    def convert_data_to_ascii(self):
        logging.info("[WASPY.IBA.ERD_SETUP] Request conversion to ascii")
        self.mpa3.convert_data_to_ascii()
        logging.info("[WASPY.IBA.ERD_SETUP] Conversion to ascii done")

    def get_measuring_time(self):
        return self.mpa3.get_measurement_time()

    @preemptive
    def _acquisition_done(self):
        while True:
            time.sleep(1)
            yield
            if not self.mpa3.acquiring():
                logging.info("[WASPY.IBA.ERD_SETUP] Acquisition has completed")
                break

    @preemptive 
    def _acquisition_started(self):
        while True:
            time.sleep(1)
            yield
            if self.mpa3.acquiring():
                logging.info("[WASPY.IBA.ERD_SETUP] Acquisition has started")
                break



def _load_flt_data(content: str) -> np.array:
    """
    Converts flt data string to numpy array
    """    
    lines = content.split('\n')
    if len(lines) == 0:
        raise RuntimeError()
    return np.asarray([[int(val) for val in line.split(' ')[:-1]] for line in lines[:-1]]) # ignore space at end of line and empty line at end of file


def _load_bparams_calibration(filename: Path, tof_chmin: int , tof_chmax: int) -> np.array:
    """
    Opens the bparams file and parses the contents into a numpy array.
    filename: bparams (B0, B1, B2)
    """

    if not filename.is_file():
        raise FileNotFoundError(f"Bparam file {filename} not found.")    
       
    B0 = np.zeros(tof_chmax+1)
    B1 = np.zeros(tof_chmax+1)
    B2 = np.zeros(tof_chmax+1)
    # B0[0] will be unused, equal to zero. (analog for B1[0], B2[0])

    try:
        with open(filename, 'r') as f:
            for i in range(tof_chmin - 1, tof_chmax):  # 0-based index
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) < 6:
                    continue
                ch = int(parts[0])
                B0[ch] = float(parts[2])
                B1[ch] = float(parts[3])
                B2[ch] = float(parts[4])
    except IOError:
        raise IOError(f"Error while opening bparams `{filename}` please verify the file and if you have network access.")

    return B0, B1, B2

def _load_tof_calibration(filename: Path) -> tuple[float, float]:
    """
    Opens a `Tof.in` file and returns the TOF calibration data.
    Returns (ns_ch, t_offs)
    """
 
    try:
        with open(filename, 'r') as f:
            for line in f:
                if 'TOF calibration' in line:
                    myindex = line.index(':')
                    ns_ch, t_offs = map(float, line[myindex+1:].strip().split())
                    return (ns_ch, t_offs)
    except IOError:
        raise RuntimeError(f"calibration not found in `{filename}`")


def _extend_flt_data(flt_data: np.array, B0, B1, B2, ns_ch, t_offs):
    """
    Extends the flt data with aditional columns (t_k, E_k) -> (t_k, t, E_k, m, m_k).
    `k` denotes that this unit is expressed per channel.
    """
    TOFCHMIN=1
    TOFCHMAX=8192

    output_data = []

    for line in flt_data:
        if len(line) < 2:
            continue
        try:
            ToFch = int(line[0])
            Ench = int(line[1])
            Ench = min(8000, Ench)
        except ValueError:
            continue

        if TOFCHMIN <= ToFch <= TOFCHMAX:
            idx = ToFch
            ToFns = 1.0e9 * (t_offs + ns_ch * ToFch)
            Iso_amu = B0[idx] + B1[idx]*Ench + B2[idx]*Ench*Ench
            Iso_ch = int(min(8000, max(1, int(Iso_amu * 100.0 + 0.5))))
            # 80 is the maximum atomic number allowed,
            # all data greather will be clipped

            output_data.append([ToFch, ToFns, Ench, Iso_amu, Iso_ch])

    return output_data

  
