from datetime import datetime, timedelta
from pprint import pprint
from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()
# print(os.environ["NOTION_TOKEN"])

notion = Client(auth=os.environ["NOTION_TOKEN"])

db_things = "8de9aae74c3d48f1b23e3f4c84f9637e"
db_records = "a8abde7d9df44f868ce3851a8fb66f78"

now = datetime.now()
filter_time = now - timedelta(minutes=3)


def query_last_edited(){

}

response = notion.databases.query(
    database_id=db_things,
    filter={
        "property": "On It",
        "checkbox": {
            "equals": True
        }
    }
)

response = notion.databases.query(
    database_id=db_records,
    filter={
        "and":[
            {
                "property": "Task",
                "relation": {
                    "contains": "cd11a269daaa4ddd8bdac0b1c1341372"
                }
            },
            {
                "property": "End At",
                "date": {
                    "is_empty": True # something is in progress
                }
            },

        ]
    }
)

print(len(response["results"]))

pprint(response)

# print(respfrom datetime import datetime
# import json
# response = json.loads(response)

# print(response['object'])
# results = response['results']

# for m in results:
#     notion.pages.create(
#         parent={
#             "type": "database_id",
#             "database_id": "a8abde7d9df44f868ce3851a8fb66f78"
#         },
#         title="hello",
#         properties={
#             "Name": {
#                 "title": [
#                     {
#                         "text": {
#                             "content": "GOGOGO"
#                         }
#                     }
#                 ]
#             },
#             "Time Frame": {
#                 "date": {
#                     "start": datetime.now().isoformat(),
#                     "end": datetime.now().isoformat()
#                 }
#             },
#             "Task": {
#                 "relation": [
#                     {"id": m['id']}
#                 ],
#             }
#         }
#     )



# my_date = datetime.now()
# print(my_date.isoformat())


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
