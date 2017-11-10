# YouTube-Backup
**This tool simply makes a backup of your playlists and channel subscriptions.** 
It doesn't make a backup of your watch later list or your history due to YouTube's API limitations.

It backups your playlists and channel subscriptions by extracting names and URL links. It then saves the data to two CSV files.


My motivation for this project is when my 10+ year old account got permentantly deleted without a warning. I lost a lot of memories that was stored in the playlists and i don't want that to happen again.


# Getting this project up and running

**Running the executable** - Jump to create an API key

**Using the Python script** - You will need to install the google API, which can be easily installed using:

`$ pip install --upgrade google-api-python-client`

or

`$ easy_install --upgrade google-api-python-client`

---

**Regardless of whether you're using the Python script or the executable, you will need to create your own API key for Google/YouTube. I've outlined the steps, so it should be easy to obtain.**


## Create an API key

Go to this Google Developers website https://console.developers.google.com/project/_/apiui/apis/library

- Click 'Create'
- Name your project
- Once the project has been created go to the API Library
- Choose the 'YouTube Data API v3' API
- Click on 'Enable'
- Click 'Create credentials' in the top right corner
- Click 'Other UI' for 'Where will you be calling the API from?'
- Click 'User Data' for 'What data will you be accessing?'
- Click 'What credentials do i need?'
- Enter a name for your client ID. 
- Click 'Create client ID'
- Enter a name for the API. This will appear when you authorize the script to access your data when you run it for the first time.
- Click 'Continue'
- Then click 'Download'

Google will download a file to your computer called 'client_id.json'. Rename this to' Google_secret.json' and place the json file in the same folder as the python script/the executable.

**You should now be good to go. :)**

## Running the tool

The tool will open up in a command window when you run it.

The first time you run the tool, you'll be given a Google URL that you need to visit. The Google URL gives the tool access to your YouTube channel, without the access, the tool will not be able to operate. 
Follow the steps given by Google and paste the code given by Google in to the command window and hit enter. You will only need to do this once unless you delete the newly created 'Google_credentials.obj' file saved in the same directory as the Python script/executable. 

The tool will then go through your channel subscriptions and playlists extracting names and URL links. It will then save this data to two CSV files, one for your channel subscriptions and one for your playlists.

