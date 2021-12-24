import re


class CloneMonitor:

    _CLONE_PROGRESS = {
        "STARTED": 15,
        "Cloning": 30,
        "remote": 70,
        "Receiving": 85,
        "Resolving": 95,
        "Checking": 100,
        "FINISHED": 100,
    }

    @classmethod
    @property
    def starting_percent(cls) -> str:
        return str(cls._CLONE_PROGRESS["STARTED"])

    @classmethod
    @property
    def finished_percent(cls) -> str:
        return str(cls._CLONE_PROGRESS["FINISHED"])

    @classmethod
    def progress(cls, line: str) -> str:
        return str(cls._CLONE_PROGRESS[cls.first_word_of(line)])

    @classmethod
    def percent(cls, stage) -> str:
        return str(cls._CLONE_PROGRESS[stage])

    @classmethod
    def first_word_of(cls, line: str) -> str:
        return re.match(r"^[A-Za-z]+", line).group(0)
