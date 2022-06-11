from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from pprint import pprint
from notion_client import Client
from dotenv import load_dotenv
import os

PROP_STARTED_AT = "Started At"
PROP_ENDED_AT = "Ended At"

load_dotenv()
# print(os.environ["NOTION_TOKEN"])

notion = Client(auth=os.environ["NOTION_TOKEN"])

db_things = "8de9aae74c3d48f1b23e3f4c84f9637e"

# db_records = "a8abde7d9df44f868ce3851a8fb66f78"

now = datetime.now(timezone.utc)
filter_time = now - timedelta(minutes=3)
print(filter_time.isoformat())


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
    # 2022-06-10T06:06:00.000Z
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


# def on_it_true_process(page):


# last edit
# [on it] is True -> (R) Record end time is empty -> do nothing -> otherwise, (C) create a new record
# [on it] is False -> (R) if Record end time is empty -> (U) fill the end time -> otherwise, do nothing
# response = query_last_edited(filter_time)
# print(response)

# response = notion.databases.query(
#     database_id=db_things,
#     filter={
#         "property": "On It",
#         "checkbox": {
#             "equals": True
#         }
#     }
# )

# response = notion.databases.query(
#     database_id=db_records,
#     filter={
#         "and":[
#             {
#                 "property": "Task",
#                 "relation": {
#                     "contains": "cd11a269daaa4ddd8bdac0b1c1341372"
#                 }
#             },
#             {
#                 "property": "End At",
#                 "date": {
#                     "is_empty": True # something is in progress
#                 }
#             },

#         ]
#     }
# )

# print(len(response["results"]))

# pprint(response)

# print(respfrom datetime import datetime
# import json
# response = json.loads(response)

# print(response['object'])
# results = response['results']

# for m in results:
    # notion.pages.create(
    #     parent={
    #         "type": "database_id",
    #         "database_id": "a8abde7d9df44f868ce3851a8fb66f78"
    #     },
    #     title="hello",
    #     properties={
    #         "Name": {
    #             "title": [
    #                 {
    #                     "text": {
    #                         "content": "GOGOGO"
    #                     }
    #                 }
    #             ]
    #         },
    #         "Time Frame": {
    #             "date": {
    #                 "start": datetime.now().isoformat(),
    #                 "end": datetime.now().isoformat()
    #             }
    #         },
    #         "Task": {
    #             "relation": [
    #                 {"id": m['id']}
    #             ],
    #         }
    #     }
    # )


my_date = datetime.now()
print(my_date.isoformat())


# notion.pages.create(
#     parent={
#         "type": "database_id",
#         "database_id": "a8abde7d9df44f868ce3851a8fb66f78"
#     },
#     title="hello",
#     properties={
#         "Name": {
#             "title": [
#                 {
#                     "text": {
#                         "content": "GOGOGO"
#                     }
#                 }
#             ]
#         },
#         "Time Frame": {
#             "date": {
#                 "start": datetime.now().isoformat(),
#                 "end": datetime.now().isoformat()
#             }
#         },
#         "Task": {
#             "relation": [
#                 {"id": "9b1e95e7dc774d52acac7f7021468d2b"}
#             ],
#         }
#     }
# )
