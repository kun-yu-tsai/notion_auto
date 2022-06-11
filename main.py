from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from notion_client import Client
from dotenv import load_dotenv
import os

PROP_STARTED_AT = "Started At"
PROP_ENDED_AT = "Ended At"

load_dotenv()

notion = Client(auth=os.environ["NOTION_TOKEN"])
db_things = os.environ["DB_THINGS"]

now = datetime.now(timezone.utc)
filter_time = now - timedelta(minutes=5)


def query_last_edited(filter_time: datetime):
    response = notion.databases.query(
        database_id=db_things,
        filter={
            "and": [
                {
                    "timestamp": "last_edited_time",
                    "last_edited_time": {
                        "after": filter_time.isoformat()
                    }
                },
                {
                    "property": "Type",
                    "select": {
                        "is_empty": True
                    }
                }
            ]

        }
    )

    return response["results"]


def get_last_edited_taipei_time(page):
    time_string_len = len("2022-06-10T06:06:00")
    last_edited_time = page['last_edited_time'][0:time_string_len]

    utc_time_with_tz = datetime.fromisoformat(
        last_edited_time).replace(tzinfo=ZoneInfo("UTC"))
    last_edited_tp_time = utc_time_with_tz.astimezone(
        tz=ZoneInfo("Asia/Taipei")).isoformat()
    
    return last_edited_tp_time

def parse_page(page):

    last_edited_tp_time = get_last_edited_taipei_time(page)
    on_it = page["properties"]["On It"]["checkbox"]

    if on_it:
        parse_when_on_it_true(page, last_edited_tp_time)
    else:
        parse_when_on_it_false(page, last_edited_tp_time)


def parse_when_on_it_true(page, last_edited_tp_time):
    page_id = page['id']
    records = query_empty_end_at_record(page_id)

    if len(records) == 0:
        page_title = page['properties']['Name']['title'][0]['text']['content']
        create_record_with(page_id, page_title, last_edited_tp_time)


def parse_when_on_it_false(page, last_edited_tp_time):
    page_id = page['id']
    records = query_empty_end_at_record(page_id)

    if len(records) != 0:
        for record in records:
            record_id = record['id']
            update_record_end_at(record_id, last_edited_tp_time)


def update_record_end_at(page_id, last_edit_stamp):
    notion.pages.update(
        page_id=page_id,
        properties={
            PROP_ENDED_AT: {
                "date": {
                    "start": last_edit_stamp,
                    # "time_zone": "Asia/Taipei"
                }
            }
        }

    )


def create_record_with(page_id, title, last_edit_stamp):
    notion.pages.create(
        parent={
            "type": "database_id",
                    "database_id": db_things
        },
        properties={
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            PROP_STARTED_AT: {
                "date": {
                    "start": last_edit_stamp,
                    # "time_zone": "Asia/Taipei"
                }
            },
            "Task": {
                "relation": [
                    {"id": page_id}
                ],
            },
            "Type":{
                "select":{
                    "name": "時間紀錄"
                }
            }
        }
    )


def query_empty_end_at_record(page_id):
    response = notion.databases.query(
        database_id=db_things,
        filter={
            "and": [
                {
                    "property": "Task",
                    "relation": {
                        "contains": page_id
                    }
                },
                {
                    "property": PROP_ENDED_AT,
                    "date": {
                        "is_empty": True  # something is in progress
                    }
                },

            ]
        }
    )

    return response['results']


last_edit_results = query_last_edited(filter_time)

for page in last_edit_results:
    parse_page(page)
