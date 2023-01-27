from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from langchain import GoogleCalendarAPIWrapper

app = FastAPI()
calendar = GoogleCalendarAPIWrapper()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/prompt")
@app.options("/prompt")
async def prompt(query: str) -> dict:
    # return {"message": "Hello World"}
    return {"response": f"{calendar.run(query)}"}


@app.post("/streamed_prompt")
@app.options("/streamed_prompt")
async def streamed_prompt(query: str, temperature: float = 0.7) -> StreamingResponse:
    response = StreamingResponse(
        content=calendar.run_sequential(query, temperature=temperature),
        status_code=200,
        media_type="text/html",
    )
    return response
