### Running the server

1. Put your Google Developer Account credentials.json
   - Needs to have permission to access the calendar in the domain
2. Run the server
3. Run the server:
```shell
cd hackathon
source entrypoint.sh                        
INFO:     Will watch for changes in these directories: ['/Users/szon/Projects/langchain/hackathon']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [9133] using StatReload
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?...
```
3. Authorize the application with an account from the same domain as the Google Developer Account.