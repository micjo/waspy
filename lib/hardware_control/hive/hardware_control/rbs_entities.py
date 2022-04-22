from typing import List, Dict, Optional
from pydantic import BaseModel, Field

from hive.hardware_control.hw_entities import HardwareUrl


class CaenDetectorModel(BaseModel):
    board: str
    channel: int
    identifier: str = Field(
        description="This will be used in the filenames for storage and in the plots for titles")
    bins_min: int
    bins_max: int
    bins_width: int = Field(
        description="The range between min and max will be rescaled to this value, The bins are combined with integer "
                    "sized bin intervals. values on the maximum side are potentially discarded")


class RbsHardwareRoute(BaseModel):
    aml_x_y: HardwareUrl
    aml_phi_zeta: HardwareUrl
    aml_det_theta: HardwareUrl
    caen: HardwareUrl
    motrona_charge: HardwareUrl


class HistogramData(BaseModel):
    data: List[int]
    title: str


class RbsData(BaseModel):
    aml_x_y: Dict
    aml_phi_zeta: Dict
    aml_det_theta: Dict
    caen: Dict
    motrona: Dict
    detectors: List[CaenDetectorModel]
    histograms: List[HistogramData]
    measuring_time_msec: str
    accumulated_charge: str


class PositionCoordinates(BaseModel):
    x: Optional[float]
    y: Optional[float]
    phi: Optional[float]
    zeta: Optional[float]
    detector: Optional[float]
    theta: Optional[float]

    def __str__(self):
        return "position_{x}_{y}_{phi}_{zeta}_{det}_{theta}".format(x=self.x, y=self.y, phi=self.phi, zeta=self.zeta,
                                                                    det=self.detector, theta=self.theta)


class RbsHistogramGraphData(BaseModel):
    graph_title: str
    histograms: List[HistogramData] = Field(
        description="For each item in this list, a new graph is created.  There is 1 plot per graph")
    x_label: str = "energy level"
    y_label: str = "yield"


class RbsHistogramGraphDataSet(BaseModel):
    """
        The amount of items in the super-list of histograms determines how many graphs will be created. The data in the"
        sub-list of histograms will be plot on the same graph. There can be more than 1 plot per graph")
        Example:
            histograms = [ [[0,1,2], [1,2,3]], [[2,3,4], [3,4,5]], [[4,5,6], [5,6,7]] ]
                           ---- graph 1 ----   ---- graph 2 -----  ---- graph 3 -----
                           -plot 1-  -plot 2-  -plot 1-  -plot 2-  - plot 1-  -plot 2-
    """

    graph_title: str
    histograms: List[List[HistogramData]]
    x_label: str = "energy level"
    y_label: str = "yield"
