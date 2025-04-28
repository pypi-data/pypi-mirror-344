import datetime
from typing import Optional

from src.million_verifier.enums import MVStatus
from src.million_verifier.responses import MVResponse


class MVFileResponse(MVResponse):
    status: Optional[MVStatus] = None

    error: Optional[str] = None

    updated_at: Optional[datetime.datetime]
    createdate: Optional[datetime.datetime]
    estimated_time_sec: Optional[int]

    def __init__(self, data):
        super().__init__(data)
        self.status = None if self.status is None else MVStatus(self.status)
        if hasattr(self, 'updated_at') and isinstance(self.updated_at, str):
            self.updated_at = datetime.datetime.strptime(self.updated_at, "%Y-%m-%d %H:%M:%S")
        if hasattr(self, 'createdate') and isinstance(self.createdate, str):
            self.createdate = datetime.datetime.strptime(self.createdate, "%Y-%m-%d %H:%M:%S")