# SduiAPI
### A simple wrapper for the SduiAPI
![discord](https://img.shields.io/discord/865504310010839080?label=discord&style=flat-square)
[![GitHub issues](https://img.shields.io/github/issues/AnnikenYT/SduiAPI?style=flat-square)](https://github.com/AnnikenYT/SduiAPI/issues)
[![GitHub forks](https://img.shields.io/github/forks/AnnikenYT/SduiAPI?style=flat-square)](https://github.com/AnnikenYT/SduiAPI/network)
[![GitHub stars](https://img.shields.io/github/stars/AnnikenYT/SduiAPI?style=flat-square)](https://github.com/AnnikenYT/SduiAPI/stargazers)

## We aren't associated with Sdui GMBH in any way!

#### TODO:
- [ ] Upload to pip

## Features:
- [x] Pull data from the [Sdui API](https://api.sdui.de/)
- [x] Parse the data to a readable format
- [x] Check if data is outdated
- [x] Sort data (Currently Only in [CLI](sdui-api-core/main.py))
- [x] Process cancellations of lessons
- [x] Add to [google calendar](https://calendar.google.com/)


## Requirements
* Python 3.*
* PIP
* The "colorama" package. To install this, use:
* Google desktop credentials (optional)
* The SduiAPI packet (optional, installation information [here]("#Wrapper"))

```bash
python3 -m pip install colorama
```

## Setup <a id="setup"></a>
* [Download](https://github.com/AnnikenYT/SduiAPI/releases/) the code as a ZIP file.
* Extract the file to a location where you find it again.
* Create a file called `secrets.py` in a location where you can remember it. You will need to copy it later.
![secrets.py file location](/docs/images/secrets.png)
* Now you need a bearer token. If you need help with that, check [here](#Bearer)
* Open the secrets.py file in your favorite text editor.
* Copy and paste the text below into the file and replace "YOUR_BEARER_TOKEN_HERE" with your Bearer token.

```py
token = "YOUR_BEARER_TOKEN_HERE"
```

If you are a bit more advanced, you can also use libraries like "cryptography" to encrypt your token.
* Now, follow the tutorials on [Wrapper usage](#Wrapper) if you want to use this in your own project, or [CLI usage](#CLI). If you just want to use the prebuild calendar extention, check [Calendar extention usage](#Calendar)



## <a id="CLI"></a>CLI usage
To use the CLI, you need to know your Timetable ID.
* Open the [Sdui Webapp](https://sdui.app) again.
* Switch to your Timetable
* Take a look at the URL Bar. You can find the ID here: **sdui.app/timetable/users/<YOUR_ID>**
![Url Bar](/docs/images/url.png)
* Copy it, and open the `main.py` file in the `sdui_api_cli`.
* At the very top, you'll find a section called "Variables". You have to paste your ID here (there is also an explanation what the Values do.):

```py
### Variables ###

TABLE_ID = <YOUR_ID> # Your Timetable ID
TIME_DELTA = 0 # Time difference in days. The value gets subtracted from the current day (1 is yesterday, 2 is 2 days ago etc.). You can use negative values to see future days.
MAX_DATA_LIFETIME = 3600 # The maximum lifetime of the data in seconds. If the data file is older that this value, the code will get a new file from the Sdui Website. A value lower than 3600 is not recommended, since it might lead to the webside thinking you are a Bot.
DEBUG = False # You don't really have to touch this, unless you want do contribute, and if you do, you probably can see what this is doing.
```

## <a id="Calendar"></a>Calendar extention usage
* To use the Calendar extention, simply copy the `secrets.py` file from [setup]("#setup") to the `sdui_api_google_calendar_extention` folder.
* Next, you need google desktop credentials. To get them, refer to [this](sdui_api_google_calendar_extention) guide.
* rename your downloaded credentials to `credentials.json` and put them in the `sdui_api_google_calendar_extention` folder.
* Now, you need your Table ID. To get it, use the [CLI]("#CLI") usage guide.
* Once you got your table id, open the `main.py` file in the `sdui_api_google_calendar_extention` folder.
* You'll need to paste the ID as described below this guide in the codebox.
* If you want to use a calendar thats not you default calendar, go to your calendar, open the calendar settings and go to `Integrate calendar`.
From there, copy the Calendar-ID at the very top. It should look like an email adress.
* Paste the Calendar-ID as described below. If you want to use your default calendar, set the `CALENDAR_ID` to `"primary"`.

```py
### Variables ###

CALENDAR_ID = "<YOUR_CALENDAR_ID_HERE>"
TIME_DELTA = -7
TABLE_ID = <YOUR_TABLE_ID_HERE>
```

## <a id="Wrapper"></a>Wrapper usage
- [ ] Coming soon!

## <a id="Bearer"></a>Get your bearer token
To get your bearer token, you need to follow these steps:
* First, login on the [Sdui-WebApp](https://sdui.app).**Do not switch to the timetable view.**
* Press `F12` on your keyboard.
You should see a screen like this pop up at the side of your screen:
![Devpanel](/docs/images/devpanel.png)
* On the very top, switch to the "Network" tab.
* Press `Shift` and `F5` to reload the page.
You will see a lot of things pop up bottom of the page. Click in the `Filter` box at the top, and type in "family. The items should reduce to two. Click on the 2nd one.
You will see a window like this one pop up:
![Headerspanel](/docs/images/header.png)
* Scroll down till you see "Request Headers", and then scroll down a bit more until you see the "authorization:" header.
* Right-click the header and select "Copy Value".
The value should look something like this (This is not a real token, it won't work with this program.):

```
Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImVjY3B1YiI6IlJVTkxNU0FBQUFBTEhaYnpUUjVTa0F6WWZ6a0dyQnh2OTJiQlA3OGVvcERiSkxtUFdOVUc2NzJmTHlkdk9vR1RUSXZ3MFlsZlI2X0dPUFVIWkhUTnRSc29paUhBR1ZiMSJ9.eyJzdWIiOiIweDQxMWZkN2QyOTFjMTg1NDg1Njc1ZDhmYWRkNzkzNDFmODkyMWYwMmIiLCJVc2VyUHViS2V5IjoiMHgwNDYxMzMyM2E0ZDhjODkzNjhkMGQ3YzU2MmVjNTM3OGNmMTRlZTRjMDQwMTU2MzcxNTQyMDVmNWIxNGZlN2RkYmM2MWRhNGM2ZjI1NjZiNGI4NzFhZmRhNDI2MDcwZDVmN2U1MzdlYmU3NDI5ODRkYzQ4MTZmZjlkMDIzNzljMmE3IiwiYXVkIjoiMHhkNjg2MDhkOGU5NjBhN2UxM2YyNzU2ZjUwOGM3MzcxZTAzYmExNzZmIiwiYXV0aF90aW1lIjoiMTYwNzcwNjgxMyIsImlhdCI6IjE2MDc3MDY4MTIiLCJzY29wZSI6WyJvcGVuaWQiLCJlbWFpbCJdLCJleHAiOiIxNjEzNzE2NzcyIiwibm9uY2UiOiI5ZTE0MDUzNTYzNmQ0YTA4OWQwNTQ0NGUzMzAxOTNiMyIsImNsaWVudF9pZCI6IjB4ZDY4NjA4ZDhlOTYwYTdlMTNmMjc1NmY1MDhjNzM3MWUwM2JhMTc2ZiIsImdyYW50X3R5cGUiOiJwYXNzd29yZCJ9.nsXQCdM5Lju5KMEf6PAXmZRHFwOMpu92Uy5JCrpUy5d0B8c9_3B1Pk3XsKJZo7knvEqYnqfpbGIEPtgayaN79Q
```

* Congratulations! You have your bearer token now! You can now proceed with the rest of the tutorial.
