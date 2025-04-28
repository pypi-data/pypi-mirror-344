from enum import Enum


class MVStatus(Enum):
    none = ""
    in_progress = "in_progress"
    success = "success"
    unknown = "unknown"