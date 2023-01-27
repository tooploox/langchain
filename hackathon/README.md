### Running the server

1. Put your Google Developer Account credentials.json in `/hackathon/credentials.json`
   - Needs to have permission to access Google Calendar in the desired domain
2. Run `poetry install`
3. Install additional packages using pip:
```shell
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
4. Add a `.env` file
```shell
cp hackathon/example.env hackathon/.env
```
5. Paste the OPENAI_API_KEY to `.env`
6. Run the server:
```shell
cd hackathon
source entrypoint.sh                        
INFO:     Will watch for changes in these directories: ['/Users/szon/Projects/langchain/hackathon']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [9133] using StatReload
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?...
```
3. Authorize the application with an account from the same domain as the Google Developer Account.