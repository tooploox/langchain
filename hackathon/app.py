from dotenv import load_dotenv
from fastapi import FastAPI

from langchain import GoogleCalendarAPIWrapper

app = FastAPI()
calendar = GoogleCalendarAPIWrapper()
load_dotenv()


@app.post("/prompt")
async def prompt(query: str) -> dict:
    # return {"message": "Hello World"}
    return {"response": f"{calendar.run(query)}"}
