"""Example to write to a Google Sheet as a Service Account."""
import os

from sheets_manager import Sheets


def main():
    """
    Write to Google Sheet.

    Ensure to export your credentials path, Google
    Sheet ID, and Spreadsheet data range before executing.
    $ export GOOGLE_SHEETS_CREDENTIALS="path/to/your/creds.json"
    $ export SHEET_ID="your-spreadsheet-id"
    $ export DEFAULT_RANGE="your-named-range"
    """
    spreadsheet = Sheets(
        scopes=["https://www.googleapis.com/auth/spreadsheets"],  # Read & write scope
        default_range=os.environ["DEFAULT_RANGE"],
    )

    data = [
        {
            "First Name": "John",
            "Last Name": "Smith",
            "Age": "32",
            "Role": "Analyst",
        },
        {
            "First Name": "Jane",
            "Last Name": "Doe",
            "Age": "35",
            "Role": "Engineer",
        },
    ]

    response = spreadsheet.as_list(data).write_data()
    print(response)


if __name__ == "__main__":
    main()
