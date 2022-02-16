from typing import Dict


class RqmActionPlan:
    def execute(self) -> None:
        raise NotImplementedError("")

    def serialize(self) -> Dict:
        raise NotImplementedError("")

    def abort(self) -> None:
        raise NotImplementedError("")

    def empty(self) -> bool:
        raise NotImplementedError("")

    def completed(self) -> bool:
        raise NotImplementedError("")


class EmptyRqmActionPlan(RqmActionPlan):
    def execute(self):
        pass

    def serialize(self):
        return ""

    def abort(self):
        pass

    def empty(self):
        return True

    def completed(self):
        return True


empty_action_plan = EmptyRqmActionPlan()