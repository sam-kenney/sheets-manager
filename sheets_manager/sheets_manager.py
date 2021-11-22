"""Functions to utilise the Google Sheets client library."""
import os
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class Sheets:
    """Operate on Google Sheets client library."""

    def __init__(
        self,
        scopes: List[str] = ["https://www.googleapis.com/auth/spreadsheets"],
        sheet_id: str = None,
        credentials: str = os.path.join(".", "credentials.json"),
        token: str = os.path.join(".", "token.json"),
        default_range: str = None,
        auth_as_service_account: bool = True,
    ) -> None:
        """
        Initialise the Class.

        args:
            scopes: List[str]
                A list of scopes determining the
                permissions granted to the code.
                Defaults to read & write.

                Scopes available here:
                https://developers.google.com/sheets/api/guides/authorizing

            sheet_id: str
                The ID of the spreadsheet to
                read from / edit.

            credentials: str
                Path to the credentials file
                to use to authenticate.
                Defaults to credentials.json

            token: str
                Path to the token file
                used to authenticate.
                Defaults to token.json

            default_range: str
                The name of the range
                to read data from.
                Must include header row.

            auth_as_service_account: bool
                Whether your credentials
                are those of a service
                account or not. Defaults
                to True.
        """
        self.credentials = os.environ.get(
            "GOOGLE_SHEETS_CREDENTIALS",
            credentials,
        )
        self.sheet_id = os.environ.get(
            "SHEET_ID",
            sheet_id,
        )
        self.default_range = default_range
        self.scopes = scopes
        self.token = token
        self.service_account = auth_as_service_account

    def _authenticate_as_user(self) -> str:
        """Set or create credentials for operations on Google Sheets."""
        credentials = None
        if os.path.exists(self.token):
            credentials = Credentials.from_authorized_user_file(
                self.token,
                self.scopes,
            )

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials,
                    self.scopes,
                )
                credentials = flow.run_local_server(port=0)

            with open(self.token, "w") as token:
                token.write(credentials.to_json())
        return credentials

    def _authenticate_as_service_account(self) -> str:
        """Authenticate using service account credentials."""
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials,
            self.scopes,
        )
        return credentials

    def spreadsheet(self):
        """Create a Spreadsheet object."""
        service = build(
            "sheets",
            "v4",
            credentials=self._authenticate_as_service_account()
            if self.service_account
            else self._authenticate_as_user(),
        )
        return service.spreadsheets()

    def _set_data_range(self, data_range: str) -> str:
        """
        Set the data range to read / write data to.

        data_range: str
            The data range passed into either
            the read or write function.

        return: str
            The data range to use.

        except: ValueError
            If no data range is
            provided.
        """
        _range = data_range or self.default_range
        if not _range:
            raise ValueError("No data range provided")
        return _range

    def read_data(self, data_range=None) -> List[list]:
        """
        Read data from the created spreadsheet object.

        data_range: str
            The name of the range
            to read data from.
            Must include header row.

        return: List[list]
            Values from the spreadsheet
            or if none found, an empty
            list.

        except: ValueError
            If no data range is provided
        """
        result = (
            self.spreadsheet()
            .values()
            .get(
                spreadsheetId=self.sheet_id,
                range=self._set_data_range(data_range),
            )
            .execute()
        )
        self.data = result.get("values", [])
        return self

    def write_data(
        self,
        data: List[list] = None,
        data_range: str = None,
    ) -> dict:
        """
        Write data to the created spreadsheet object.

        data: List[list]
            The data to write to the spreadsheet.

        data_range: str
            The name of the range
            to write data to.

        return: dict
            Information about the write operation
            including the spreadsheet ID,
            and number of rows written.

        except: ValueError
            If no data range is provided
        """
        _data = data or self.data
        response = (
            self.spreadsheet()
            .values()
            .update(
                spreadsheetId=self.sheet_id,
                valueInputOption="RAW",
                range=self._set_data_range(data_range),
                body=dict(values=_data),
            )
            .execute()
        )
        return response

    def as_dict(self, data: List[list] = None) -> List[dict]:
        """
        Convert data extracted from a Google Sheet into a list of dicts.

        Allows for chaining of other methods.

        args:
            data: List[list]
                The raw data extracted from Google Sheets.

        return:
            The data parsed as a list of dicts.
        """
        _data = data or self.data
        if _data and isinstance(_data, list):
            headers = _data[0]

            return [
                {
                    header: value if value else None
                    for header, value in zip(
                        headers,
                        row,
                    )
                }
                for row in _data
                if row is not headers
            ]
        else:
            raise ValueError("No data provided")

    def as_list(self, data: List[dict] = None, header: bool = True) -> List[list]:
        """
        Convert list of dicts into the correct format to write to a sheet.

        Allows for chaining of other methods.

        args:
            data: List[dict]
                A list of dictionaries to convert
                into a list of lists to write.

            header: bool
                Optional parameter to include or
                exclude the header row when
                converting to sheets formatted
                data. Defaults to True (include).

        return: List[list]
            Data formatted to be written to
            a spreadsheet.
        """
        _data = data or self.data
        if _data and isinstance(_data, list):
            self.data = (
                [list(data[0].keys())] + [list(row.values()) for row in data]
                if header
                else [list(row.values()) for row in data]
            )

            return self
        else:
            raise ValueError("No data provided")

    @staticmethod
    def to_dict(data: List[list]) -> List[dict]:
        """
        Convert a list of lists into a list of dicts.

        args:
            data: List[list]
                The raw data extracted from Google Sheets.

        return:
            The data parsed as a list of dicts.
        """
        headers = data[0]

        return [
            {
                header: value if value else None
                for header, value in zip(
                    headers,
                    row,
                )
            }
            for row in data
            if row is not headers
        ]

    @staticmethod
    def to_list(data: List[dict], header: bool = True) -> List[list]:
        """
        Convert list of dicts a list of lists.

        args:
            data: List[dict]
                A list of dictionaries to convert
                into a list of lists to write.

            header: bool
                Optional parameter to include or
                exclude the header row when
                converting to sheets formatted
                data. Defaults to True (include).

        return: List[list]
            Data formatted to be written to
            a spreadsheet.
        """
        return (
            [list(data[0].keys())] + [list(row.values()) for row in data]
            if header
            else [list(row.values()) for row in data]
        )
