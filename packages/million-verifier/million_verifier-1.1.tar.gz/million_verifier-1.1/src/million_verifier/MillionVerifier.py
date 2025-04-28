import os
from typing import Any

import requests

from src.million_verifier.exceptions import MVClientException, MVApiException
from src.million_verifier.responses import MVGetFileResponse, MVUploadFileResponse, MVVerifyResponse


class MillionVerifier:
    BASE_URL = "https://api.millionverifier.com/api/v3"
    BULK_BASE_URL = "https://bulkapi.millionverifier.com/bulkapi/v2"

    def __init__(self, api_key: str):
        if not api_key.strip():
            raise MVClientException("Empty parameter: api_key")
        self._api_key = api_key

    def _get(self, url, response_class, params=None):
        if not params:
            params = {}
        params["key"] = self._api_key
        response = requests.get(url, params=params)
        json_response: dict[str, Any]
        try:
            json_response = response.json()
        except ValueError as e:
            raise MVApiException from e
        if json_response.get("error", None):
            error = json_response.pop("error", None)
            if error:
                raise MVApiException(error)
        return response_class(json_response)

    def _post(self, url, response_class, data=None, json=None, files=None):
        response = requests.post(url, data=data, json=json, files=files)
        try:
            json_response = response.json()
        except ValueError as e:
            raise MVApiException('Request not processed succesfully. Status code %s' % response.status_code)

        return response_class(json_response)

    def verify(self, email: str, timeout: int = 10):
        """Verify an email address in real time and get results in just a second.

        Parameters
        ----------
        email: str
            The email address you want to verify
        timeout: str or None
            Time in seconds to terminate the connection in case no response recevied from the recipient server. You can set between 2 and 60 seconds. Default timeout is 20 seconds.

        Raises
        ------
        MillionVerifierApiException

        Returns
        -------
        response: MVVerifyResponse
            Returns a MVVerifyResponse object if the request was successful
        """

        return self._get(
            f"{self.BASE_URL}/verify",
            MVVerifyResponse,
            params={
                "email": email,
                "timeout": timeout,
            },
        )


    def _upload_file(
        self,
        file_path: str,
        data: dict,
    ):
        data.update(
            {
                "key": self._api_key,
            }
        )
        url = f"{self.BULK_BASE_URL}/upload"
        files = [
            ('file_contents', ('filename', open(file_path, 'rb'), 'text/plain'))
        ]
        return self._post(url, MVUploadFileResponse, data=data, files=files)

    def upload_file(
        self,
        file_path: str,
    ):
        """Allows user to send a file for bulk email validation

        Parameters
        ----------
        file_path: str
            The path of the csv or txt file to be submitted.

        Raises
        ------
        MillionVerifierApiException

        Returns
        -------
        response: MVUploadFileResponse
            Returns a ``MVUploadFileResponse`` object if the request was successful
        """

        data = {}
        return self._upload_file(file_path, data)

    def _file_status(self, file_id: str):
        if not file_id.strip():
            raise MVClientException("Empty parameter: file_id")
        return self._get(
            f"{self.BULK_BASE_URL}/fileinfo",
            MVUploadFileResponse,
            params={"file_id": file_id},
        )

    def file_status(self, file_id: str):
        """Returns the file processing status for the file that has been submitted

        Parameters
        ----------
        file_id: str
            The returned file ID when calling sendfile API.

        Raises
        ------
        MillionVerifierClientException

        Returns
        -------
        response: MVUploadFileResponse
            Returns a ``MVUploadFileResponse`` object if the request was successful
        """

        return self._file_status( file_id)

    def _get_file(self, file_id: str, download_path: str, filter: str):
        if not file_id.strip():
            raise MVClientException("Empty parameter: file_id")
        response = requests.get(
            f"{self.BULK_BASE_URL}/download",
            params={
                "key": self._api_key,
                "file_id": file_id,
                "filter": filter
            },
        )
        if response.headers["Content-Type"] == "application/json":
            json_response = response.json()
            return MVGetFileResponse(json_response)

        dirname = os.path.dirname(download_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(download_path, "wb") as f:
            f.write(response.content)

        return MVGetFileResponse({"local_file_path": download_path})

    def get_file(self, file_id: str, download_path: str):
        """Allows you to get the validation results for the file you submitted

        Parameters
        ----------
        file_id: str
            The returned file ID when calling sendfile API.
        download_path: str
            The local path where the file will be downloaded.

        Raises
        ------
        MVClientException

        Returns
        -------
        response: MVGetFileResponse
            Returns a MVGetFileResponse object if the request was successful
        """

        return self._get_file(file_id, download_path, 'all')