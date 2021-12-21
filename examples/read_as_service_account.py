"""Example to read from a Google Sheet as a Service Account."""
from sheets_manager import Sheets


def main():
    """
    Read from a Google Sheet.

    Ensure to export your credentials path before executing.
    `export GOOGLE_SHEETS_CREDENTIALS="path/to/your/creds.json"`
    """
    spreadsheet = Sheets(
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets.readonly"
        ],  # Readonly scope
        sheet_id="1ivbBDpVF2NJRFOCv_87nUic3iEHlvHQ_AhJbvyvt1bk",
        default_range="employees",
    )

    data = spreadsheet.read_data().as_dict()
    print(data)


if __name__ == "__main__":
    main()
