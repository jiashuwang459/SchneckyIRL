# SchneckyIRL



# Prereqs

* Python 3.x
* DiscordPy
* Google Sheets API


## Discord Python API 

### (Recommended) Setup a pyenv
```bash
python3 -m venv bot-env
```
#### To Activate:
##### Linux:
```bash
source bot-env/bin/activate
```
##### Windows:
```bash
bot-env\Scripts\activate.bat
```

### Install Discord Dependencies
more info [here](https://discordpy.readthedocs.io/en/stable/intro.html)

```bash
pip install -U discord.py
```

## Google Sheets API
### Install dependencies
more info [here](https://developers.google.com/sheets/api/quickstart/python)

```bash
#Note: make sure your pip version is 3.x. Alternatively, use pip3. If you're using a pyenv, make sure it's activated
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
### Create your credentials.json file
more info [here](https://developers.google.com/workspace/guides/create-credentials)

1. Go to https://console.cloud.google.com/ and create a new project (or use an existing one).
1. Go to `APIs & Services` > `OAuth consent screen`
	1. Click `External` User Type, and fill in all of the required information
1. Go to `APIs & Services` > `Credentials` > `Create Credentials` > `OAuth Client ID`
	1. Fill in the required information. Once you're done, you should be brought back to the `Credentials` page.
1. Under OAuth 2.0 Client IDs, you should now have a new Client ID. Go to the right and click download.
1. rename the file to `credentials.json` and place it in the root directory of this reposity.


### Configuring Bot Token And SpreadSheetId

You need to setup 2 env_vars:

`STAT_BOT_TOKEN` should be your discord bot token.
`SPREADSHEET_ID` should be the id of the google spreadsheet.

Alternatively, you can create two additional 2 files: `bottoken.txt` and `spreadsheetid.txt`:

`bottoken.txt` should contain your discord bot token.
`spreadsheetid.txt` should contain the id of the spreadsheet.


Afterwards... simpy run :D
```bash
python bot.py
```

Note: First time running will open up a tab, where you will need to allow permissions and get through Safety in accessing the spreadsheet. If you get one of those red warning insecure pages, you need to click `Advanced` > `Continue to page`.
