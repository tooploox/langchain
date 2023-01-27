"""Prompts for Google Calendar."""

CLASSIFICATION_PROMPT = """

{query}

The following is an action to be taken in a calendar.
Classify it as one of the following: \n\n
create_event \n
view_event \n
view_events \n
delete_event \n
reschedule_event \n
choice_event \n

Classification:
"""

RESCHEDULE_EVENT_PROMPT = """

Date format: YYYY-MM-DDThh:mm:ss+00:00
Based on this event description:\n'Move Joey birthday to tomorrow at 7 pm',
output a json of the following parameters: \n
Today's datetime on UTC time 2021-05-02T10:00:00+00:00 and timezone
of the user is -5, take into account the timezone of the user and today's date.

1. event_summary \n
2. event_start_time \n
3. event_end_time \n

event_summary:\n
{{
    "event_summary": "Joey birthday",
    "event_start_time": "2021-05-03T19:00:00-05:00",
    "event_end_time": "2021-05-03T20:00:00-05:00"
}}


Date format: YYYY-MM-DDThh:mm:ss+00:00
Based on this event description:\n{query}, output a json of the
following parameters: \n
Today's datetime on UTC time {date} and timezone of the user {u_timezone},
take into account the timezone of the user and today's date.


1. event_summary \n
2. event_start_time \n
3. event_end_time \n

event_summary:  \n
"""

CHOICE_EVENT_PROMPT = """
Below is the list of calendar events.

{query}

There is too many of them. I'd like to only attend one and cancel one. 
Please select the event I should attend and provide a funny explanation 
why and also select the event I should cancel and provide funny explanation. Reply in Polish.

In the format:
1. Attend event name - funny explanation why to attend
2. Cancel event name - funny explanation why to cancel
"""

DELETE_EVENT_PROMPT = """

Based on this event description:\n'Remove meeting with Joona',
output a json of the following parameters: \n

1. event_summary \n


event_summary:\n
{{
    "event_summary": "meeting with Joona"
}}


Based on this event description:\n{query}, output a json of the
following parameters: \n

1. event_summary \n

event_summary:  \n
"""

CREATE_EVENT_PROMPT = """
Date format: YYYY-MM-DDThh:mm:ss+00:00
Based on this event description:\n'Joey birthday tomorrow at 7 pm',
output a json of the following parameters: \n
Today's datetime on UTC time 2021-05-02T10:00:00+00:00 and timezone
of the user is -5, take into account the timezone of the user and today's date.

1. event_summary \n
2. event_start_time \n
3. event_end_time \n
4. event_location \n
5. event_description \n
6. user_timezone \n


event_summary:\n
{{
    "event_summary": "Joey birthday",
    "event_start_time": "2021-05-03T19:00:00-05:00",
    "event_end_time": "2021-05-03T20:00:00-05:00",
    "event_location": "",
    "event_description": "This is a celebration of Joeys bithday.",
    "user_timezone": "America/New_York"
}}


Date format: YYYY-MM-DDThh:mm:ss+00:00
Based on this event description:\n{query}, output a json of the
following parameters: \n
Today's datetime on UTC time {date} and timezone of the user {u_timezone},
take into account the timezone of the user and today's date.
Generate a probable 3-sentence funny description of the event based on its summary in the same
language as the summary.


1. event_summary \n
2. event_start_time \n
3. event_end_time \n
4. event_location \n
5. event_description \n
6. user_timezone \n

event_summary:  \n
"""

CREATE_DESCRIPTION_PROMPT = """
Create a funny description of an event, based on the given event summary, in the same language 
as the create prompt:
{query}
"""
