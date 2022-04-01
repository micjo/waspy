from typing import Dict


class Job:
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


class EmptyJob(Job):
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


empty_job = EmptyJob()
