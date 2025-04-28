from typing import Optional

from src.million_verifier.responses import MVFileResponse


class MVUploadFileResponse(MVFileResponse):
    """This is the response for the POST /upload request."""

    file_name: Optional[str] = None

    file_id: Optional[str] = None

    unique_emails: Optional[int] = 0

    percent: Optional[int] = 0

    total_rows: Optional[int] = 0

    verified: Optional[int] = 0

    unverified: Optional[int] = 0

    ok: Optional[int] = 0

    catch_all: Optional[int] = 0

    disposable: Optional[int] = 0

    invalid: Optional[int] = 0

    unknown: Optional[int] = 0

    reverify: Optional[int] = 0

    credit: Optional[int] = 0