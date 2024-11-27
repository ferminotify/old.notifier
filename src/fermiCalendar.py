import pandas as pd
import requests
import csv

from src.logger import Logger
from src.databaseOperations import get_all_sent_id
from src.utility import is_event_today
logger = Logger()

"""
Summary of all the operations involving the Fermi Calendar and its events.
"""

def get_events() -> list[dict]:
    """
    Get events from Google Sheets as a CSV file.

    This file is obtained through a Google Script that takes the events from the
    Fermi Calendar
    and puts them in a CSV file.
    The events in the file get deleted after a day to optimize the operations.

    Returns:
        list: list of dictionaries containing all the events.
    """
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSn-iVUb73XGXN7qWU0S2njYO8yl8LFv0V-1a3VTU7mPB6rJUqYasGPJcmWyc1wGvjDd7IWH3qci75l/pub?gid=0&single=true&output=csv"

    data = []
    try:
        response = requests.get(URL)
        response.raise_for_status()
        logger.debug("Successfully fetched events from Google Sheets.")

        decoded_content = response.content.decode('utf-8')
        csv_reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
        for row in csv_reader:
            data.append(row)
        logger.debug("Successfully parsed CSV data into a list of dictionaries.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching events from Google Sheets: {e}")
    except Exception as e:
        logger.error(f"Error processing CSV data: {e}")

    return data

def collect_notifications(subs: list[dict]) -> list[dict]:
    """Collect all the notifications for the subscribers.

    This function gets all the events from the Google Sheets and compares them 
    to the subscribers.
    If there is a match, the subscriber gets notified.

    Args:
        subs (list): list of dictionaries containing all the subscribers.

    Returns:
        list: list of dictionaries containing all the subscribers that need to 
        be notified and
        the corresponding events.
    """
    events = get_events()
    logger.info("Fetched events for notification collection.")

    notifications = []
    
    c = 0
    all_ids = get_all_sent_id()
    for sub in subs:
        logger.debug(f"Processing notifications for user {c}: {sub['email']}")
        usr_kw = sub["tags"]
        
        # get the sent events ids
        sent = []
        for i in all_ids:
            if str(i[1]) == str(sub["id"]):
                sent.append(i[2])

        user_events = []

        for evt in events:
            if usr_kw:
                event_title = ""
                try:
                    event_title = "".join(c for c in evt["summary"].lower()
                        if ((c.isalpha() or c.isdecimal()) or c == ' ')) + " "
                except Exception as e:
                    logger.error(f"Error processing event title: {e}")

                kw_in_subject = any(((kw.lower() + " ") in event_title
                                    for kw in usr_kw))
                # I append a space to the keyword so, for example, the user 
                # with the tag 4E doesn't receive the information about the 
                # events of 4EAU
                
                evt_not_in_db = evt["uid"] not in sent

                if kw_in_subject:
                    if is_event_today(evt):
                        if evt_not_in_db:
                            user_events.append(evt)

                # print(f"keyword of {sub['email']}: {usr_kw}")
                # print(f"event title: {event_title}")
        if len(user_events) > 0:
            notifications.append({
                "id": sub["id"],
                "name": sub["name"],
                "gender": sub["gender"],
                "email": sub["email"],
                "n_pref": sub["n_pref"],
                "telegram": sub["telegram"],
                "events": user_events
            })
            logger.info(f"User {sub['email']} has {len(user_events)} new notifications.")
        logger.debug(f"Finished processing user {c}: {sub['email']}")
        c += 1

    logger.info("Finished collecting notifications for all users.")
    return notifications
