"""Prompts for Google Calendar."""

CLASSIFICATION_PROMPT = """

{query}

The following is an action to be taken in a calendar.
Classify it as one of the following: \n\n
1. create_event \n
2. view_event \n
3. view_events \n
4. delete_event \n
5. reschedule_event \n

Classification:
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
    "event_description": "",
    "user_timezone": "America/New_York"
}}


Date format: YYYY-MM-DDThh:mm:ss+00:00
Based on this event description:\n{query}, output a json of the
following parameters: \n
Today's datetime on UTC time {date} and timezone of the user {u_timezone},
take into account the timezone of the user and today's date.


1. event_summary \n
2. event_start_time \n
3. event_end_time \n
4. event_location \n
5. event_description \n
6. user_timezone \n

event_summary:  \n
"""
