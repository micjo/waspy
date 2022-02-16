from datetime import datetime, timedelta

from pydantic import BaseModel

from app.erd.data_serializer import ErdDataSerializer
from app.erd.erd_setup import ErdSetup
from app.rqm.rqm_action_plan import RqmActionPlan


class ErdRecipeStatus(BaseModel):
    recipe_id: str
    start_time: datetime
    run_time: timedelta
    measurement_time: float
    measurement_time_target: float


empty_erd_recipe_status = ErdRecipeStatus(recipe_id="", start_time=datetime.now(), run_time=0,
                                          measurement_time=0, measurement_time_target=0)


class ErdAction(RqmActionPlan):
    _data_serializer: ErdDataSerializer
    _erd_setup: ErdSetup




