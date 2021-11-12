# Google Sheets Manager

This repository is used to manage Google Sheets.

## Credentials
Make a copy of the `env_template` file and name it `.env`. You will need to provide a Spreadsheet ID, and a path to a desktop application [credentials file](https://developers.google.com/workspace/guides/create-credentials#create_a_oauth_client_id_credential) used to authenticate agains the Sheets API.

To use the `.env` file you have created, type `source .env` into your terminal.


Variable                       | Meaning
-------------------------------|----------------------------------------------
SHEET_ID                  | Google Spreadsheet ID.
GOOGLE_SHEETS_CREDENTIALS | Path to your credentials file, either Service Account credentials, or Desktop Application credentials.


## Creating an environment
Create a virtual development environment by using the `virtualenv` Python library. You can install this by executing `pip3 install virtualenv`. 

To create your environment, type `virtualenv {your-env}`. Once created, you must activate it by using `source {your-env}/bin/activate`. Once you are done developing, simply type `deactivate` in your terminal.

## Installation
*   Install the required Python libraries using `pip3 install -r requirements.txt`.
*   If you are developing for this tool, install the Python libraries required by running `pip3 install -r dev-requirements.txt`.

*Please ensure to create your environment before you execute any of the installation commands*

## Using the Sheets Class

The `Sheets` class has a number of parameters, most of which are optional.

Parameter | Use
----------|-----
scopes| Defines the [scopes](https://developers.google.com/sheets/api/guides/authorizing) to be granted to the application. We highly recommend you only use the scopes required for each application. Defaults to read and write access.
sheet_id | The ID of the spreadsheet to edit. The class will attempt to extract this from the environment, but if you cannot set it there, you may explicitly provide it here.
credentials | The path to your Google Sheets credentials file. Defaults to `credentials.json`. The class will attempt to extract this from the environment, but if you cannot set it there, you may explicitly provide it here.
token | The name of the refresh token file. Defaults to `token.json`. We recommend you leave this as it's default.
default_range | A default range to read from or write to. If you are reading from this range, it MUST include the header row. This parameter defaults to None, and is overwritten by the optional `data_range` parameter found in the `read_data()` and `write_data()` methods. 
auth_as_service_account | Allows you to either authentiate as a service account, or as a user. Defaults to service account.

### Reading from a Spreadsheet
```py
from sheets_manager import Sheets

spreadsheet = Sheets(
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
    sheet_id="A73AscX-jJrcsRuiDkjher",
    credentials="~/credentials/credentials.json",
    default_range="accounts",
)

data = spreadsheet.read_data().to_dict()
```


### Writing to a Spreadsheet
When writing to a Spreadsheet, you must write data as a list of lists. For this, we have included a function, `to_list()`, which converts a list of dictionaries into a list of lists. With this function, there is an optional parameter of `header` which takes a `bool`. This parameter determines whether or not to write the data with the header row.

```py
from sheets_manager import Sheets

spreadsheet = Sheets(
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
    sheet_id="A73AscX-jJrcsRuiDkjher",
    credentials="~/credentials/credentials.json",
    default_range="employees"
)

data = [
    {
        "Name": "Fred",
        "Age": 31,
    },
    {
        "Name": "Julie",
        "Age": 28,
    },
]

resp = spreadsheet.to_list(data=data).write_data()
```
