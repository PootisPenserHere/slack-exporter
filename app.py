import json
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv(".env")


def _fetch(url: str, next_cursor: str = None) -> list:
    params = {
        "token": os.getenv('SLACK_TOKEN'),
        "types": "public_channel,private_channel"
    }

    if next_cursor:
        params['cursor'] = next_cursor

    raw_output = requests.get(url=url, params=params)
    output = raw_output.json()

    # Sleep to avoid hitting the api rate limit
    time.sleep(1)

    new_cursor = output['response_metadata']['next_cursor']
    if new_cursor:
        return output.get('channels') + _fetch(url, new_cursor)

    return output.get('channels')


def _save_to_file(data, file_path):
    with open(file_path, 'w') as file:
        file.write(json.dumps(data, sort_keys=False, indent=4))


channels = _fetch(url="https://slack.com/api/conversations.list")
_save_to_file(data=channels, file_path="./output/channels.json")
