"""Chain that calls Google Calendar."""

import datetime
import json
from pprint import pprint
import os
from typing import Any, Dict, List

from pydantic import BaseModel, Extra, root_validator

from langchain.utilities.google_calendar.prompts import (
    CLASSIFICATION_PROMPT,
    CREATE_EVENT_PROMPT,
    DELETE_EVENT_PROMPT, 
    CREATE_DESCRIPTION_PROMPT,
    CHOICE_EVENT_PROMPT,
    RESCHEDULE_EVENT_PROMPT,
)


class GoogleCalendarAPIWrapper(BaseModel):
    """Wrapper around Google Calendar API.

    To use, you need to create a Google Cloud project and
    enable the Google Calendar API.

    Follow instructions here:
    - https://developers.google.com/calendar/api/quickstart/python

    For pip libraries:
    - pip install --upgrade
    google-api-python-client google-auth-httplib2 google-auth-oauthlib

    OAuth2.0 done through credentials.json folder in the root directory.
    """

    service: Any  #: :meta private:
    google_http_error: Any  #: :meta private:
    creds: Any  #: :meta private:

    SCOPES: List[str] = [
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/calendar.events",
    ]

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def create_event(
        self,
        event_summary: str,
        event_start_time: str,
        event_end_time: str,
        user_timezone: str,
        event_location: str = "",
        event_description: str = "",
        # TODO: Implement later
        # event_recurrence:str=None,
        # event_attendees: List[str]=[],
        # event_reminders:str=None,
    ) -> Any:
        """Create an event in the user's calendar."""
        event = {
            "summary": event_summary,
            "location": event_location,
            "description": event_description,
            "start": {
                "dateTime": event_start_time,
                "timeZone": user_timezone,
                # utc
            },
            "end": {
                "dateTime": event_end_time,
                "timeZone": user_timezone,
            },
            # TODO: Implement later
            # "recurrence": [event_recurrence],
            # "attendees": event_attendees,
            # "reminders": event_reminders,
        }
        try:
            created_event = (
                self.service.events().insert(calendarId="primary", body=event).execute()
            )
            return created_event

        except self.google_http_error as error:
            return f"An error occurred: {error}"

    # Not implemented yet
    def view_events(self) -> Any:
        """View all events in the user's calendar."""
        try:
            import datetime

            now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            if not events:
                print("No upcoming events found.")
                return
            # for event in events:
            #     start = event['start'].get('dateTime', event['start'].get('date'))
            #     print(start, event['summary'])
            return events
        except self.google_http_error as error:
            print(f"An error occurred: {error}")

    # Not implemented yet
    def view_event(self, event_id: str) -> Any:
        """View an event in the user's calendar."""
        try:
            event = (
                self.service.events()
                .get(calendarId="primary", eventId=event_id)
                .execute()
            )
            print(f'Event summary: {event["summary"]}')
            print(f'Event location: {event["location"]}')
            print(f'Event description: {event["description"]}')
            return event
        except self.google_http_error as error:
            print(f"An error occurred: {error}")

    # Not implemented yet
    def reschedule_event(
        self, event_id: str, new_start_time: str, new_end_time: str
    ) -> Any:
        """Reschedule an event in the user's calendar."""
        try:
            event = (
                self.service.events()
                .get(calendarId="primary", eventId=event_id)
                .execute()
            )
            event["start"]["dateTime"] = new_start_time
            event["end"]["dateTime"] = new_end_time
            updated_event = (
                self.service.events()
                .update(calendarId="primary", eventId=event_id, body=event)
                .execute()
            )
            print(f'Event rescheduled: {updated_event.get("htmlLink")}')
            return updated_event
        except self.google_http_error as error:
            print(f"An error occurred: {error}")

    #Not implemented yet
    def delete_event(self, event_id: str) -> Any:
        """Delete an event in the user's calendar."""
        try:
            self.service.events().delete(
                calendarId="primary", eventId=event_id
            ).execute()
            print(f"Event with ID {event_id} has been deleted.")
        except self.google_http_error as error:
            print(f"An error occurred: {error}")

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        #
        # Auth done through OAuth2.0

        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            from googleapiclient.errors import HttpError

            SCOPES = [
                "https://www.googleapis.com/auth/calendar.readonly",
                "https://www.googleapis.com/auth/calendar.events",
            ]
            creds: Any = None
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
            values["service"] = build("calendar", "v3", credentials=creds)
            values["google_http_error"] = HttpError
            values["creds"] = creds

        except ImportError:
            raise ValueError(
                "Could not import google python packages. "
                """Please it install it with `pip install --upgrade
                google-api-python-client google-auth-httplib2 google-auth-oauthlib`."""
            )
        return values

    def run_classification(self, query: str) -> str:
        """Run classification on query."""
        from langchain import LLMChain, OpenAI, PromptTemplate

        prompt = PromptTemplate(
            template=CLASSIFICATION_PROMPT, input_variables=["query"]
        )
        llm_chain = LLMChain(
            llm=OpenAI(temperature=0, model_name="text-davinci-003"),
            prompt=prompt,
            verbose=True,
        )
        return llm_chain.run(query=query).strip().lower()

    def run_create_event(self, query: str) -> str:
        """Run create event on query."""
        from langchain import LLMChain, OpenAI, PromptTemplate

        # Use a classification chain to classify the query
        date_prompt = PromptTemplate(
            input_variables=["date", "query", "u_timezone"],
            template=CREATE_EVENT_PROMPT,
        )
        create_event_chain = LLMChain(
            llm=OpenAI(temperature=0, model="text-davinci-003"),
            prompt=date_prompt,
            verbose=True,
        )
        date = datetime.datetime.utcnow().isoformat() + "Z"
        u_timezone = str(
            datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        )
        # llm_chain.run(query=query).strip() ouputs a json string
        output = create_event_chain.run(
            query=query, date=date, u_timezone=u_timezone
        ).strip()
        
        # Temporary display event summary response from GPT
        print(output)

        # Use a classification chain to guess the description
        description_prompt = PromptTemplate(
            input_variables=["query"],
            template=CREATE_DESCRIPTION_PROMPT,
        )
        create_description_chain = LLMChain(
            llm=OpenAI(temperature=0.9),
            prompt=description_prompt,
            verbose=True,
        )
        funny_description = create_description_chain.run(query=query)

        loaded = json.loads(output)
        (
            event_summary,
            event_start_time,
            event_end_time,
            event_location,
            event_description,
            user_timezone,
        ) = loaded.values()

        event = self.create_event(
            event_summary=event_summary,
            event_start_time=event_start_time,
            event_end_time=event_end_time,
            user_timezone=user_timezone,
            event_location=event_location,
            event_description=funny_description,
        )
        return event

    def remove_common_words(self, word):
        newWord = word
        common_words = ["with", "your", "that", "what", "have", "from"]
        for i in common_words:
            newWord = newWord.replace(i, '')
        return newWord

    def lcs(self, s, t):
        s = self.remove_common_words(s)
        t = self.remove_common_words(t)
        m, n = len(t), len(s)
        dp = [[0 for i in range(m + 1)] for j in range(2)]
        res = 0
        
        for i in range(1,n + 1):
            for j in range(1,m + 1):
                if(s[i - 1] == t[j - 1]):
                    dp[i % 2][j] = dp[(i - 1) % 2][j - 1] + 1
                    if(dp[i % 2][j] > res):
                        res = dp[i % 2][j]
                else:
                    dp[i % 2][j] = 0
        return res
    
    def find_event_id_by_name(self, event_name):
        try:
            events = self.view_events()
            most_possible_event = None
            longest_lcs = 0
            for i in events:
                l = self.lcs(i["summary"], event_name)
                if l > longest_lcs:
                    longest_lcs = l
                    most_possible_event = i
            if longest_lcs < 3:
                raise Exception( "could not find matching event")
            pprint(most_possible_event)
            return most_possible_event
        except Exception as inst:
            print(inst.args)
        
    def run_delete_event(self, query) -> Any:
        """Run delete event on query."""
        from langchain import LLMChain, OpenAI, PromptTemplate

        # Use a classification chain to classify the query
        date_prompt = PromptTemplate(
            input_variables=["query"],
            template=DELETE_EVENT_PROMPT,
        )
        delete_event_chain = LLMChain(
            llm=OpenAI(temperature=0, model="text-davinci-003"),
            prompt=date_prompt,
            verbose=True,
        )
        output = delete_event_chain.run(
            query=query
        ).strip()
        loaded = json.loads(output)
        (
            event_summary,
        ) = loaded.values()
        prediction = self.find_event_id_by_name(loaded["event_summary"])
        if prediction != None:
            self.delete_event(prediction["id"])
        else:
            prediction = {"summary": "none", "id": "none"}
        return "Welp fella, that's your event name: " + loaded["event_summary"] + "\n" "I also tried to find it's id in your calendar: " + prediction["summary"] + " " + prediction["id"]
    
    def run_reschedule_event(self, query) -> Any:
        """Run create event on query."""
        from langchain import LLMChain, OpenAI, PromptTemplate

        # Use a classification chain to classify the query
        date_prompt = PromptTemplate(
            input_variables=["date", "query", "u_timezone"],
            template=RESCHEDULE_EVENT_PROMPT,
        )
        reschedule_event_chain = LLMChain(
            llm=OpenAI(temperature=0, model="text-davinci-003"),
            prompt=date_prompt,
            verbose=True,
        )
        date = datetime.datetime.utcnow().isoformat() + "Z"
        u_timezone = str(
            datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        )
        # llm_chain.run(query=query).strip() ouputs a json string
        output = reschedule_event_chain.run(
            query=query, date=date, u_timezone=u_timezone
        ).strip()
        
        # Temporary display event summary response from GPT
        
        loaded = json.loads(output)
        (
            event_summary,
            event_start_time,
            event_end_time,
        ) = loaded.values()
        pprint("printing vals from prompt")
        pprint(loaded)
        prediction = self.find_event_id_by_name(loaded["event_summary"])   
        self.reschedule_event(prediction["id"], event_start_time, event_end_time)
        return (prediction["id"], prediction["start"]["dateTime"], prediction["end"]["dateTime"])

    def run_choice_events(self) -> str:
        from langchain import LLMChain, OpenAI, PromptTemplate

        events = self.view_events()
        query = " \n".join([f"{idx+1}. {event['summary']}" for idx, event in enumerate(events)])

        choice_prompt = PromptTemplate(
            input_variables=["query"],
            template=CHOICE_EVENT_PROMPT,
        )
        choice_events_chain = LLMChain(
            llm=OpenAI(temperature=0, model="text-davinci-003"),
            prompt=choice_prompt,
            verbose=True,
        )
        output = choice_events_chain.run(
            query=query,
        ).strip()
        return output

    def run(self, query: str) -> Dict[str, Any]:
        """Ask a question to the notion database."""
        # Use a classification chain to classify the query
        classification = self.run_classification(query)

        if classification == "create_event":
            resp = self.run_create_event(query)
        elif classification == "view_events":
            resp = self.view_events()
        elif classification == "delete_event":
            resp = self.run_delete_event(query)
        elif classification == "reschedule_event":
            resp = self.run_reschedule_event(query)
        elif classification == "choice_event":
            resp = self.run_choice_events()
        else:
            return {"classification": "error", "response": f"{classification} is not implemented"}

        # TODO: reschedule_event, view_event, delete_event
        return {"classification": classification, "response": resp}
