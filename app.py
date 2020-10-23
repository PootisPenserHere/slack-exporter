import errno
import json
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv(".env")


def _fetch(url: str, desired_key: str, next_cursor: str = None, **kwargs) -> list:
    params = {
        "token": os.getenv('SLACK_TOKEN'),
    }

    if next_cursor:
        params['cursor'] = next_cursor

    # Add the extra params to the to be query string
    params = {**params, **kwargs}

    output = requests.get(url=url, params=params).json()

    # Sleep to avoid hitting the api rate limit
    time.sleep(1)

    # Some endpoints like conversations.history won't show this when there is no more items to
    # send while other endpoints like conversations.list show it as an empty string
    new_cursor = output['response_metadata']['next_cursor'] if "response_metadata" in output else None

    if new_cursor:
        return output.get(desired_key) + _fetch(url, desired_key, new_cursor, **kwargs)

    return output.get(desired_key)


def _save_to_file_as_json(data, file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(file_path, 'w') as file:
        file.write(json.dumps(data, sort_keys=False, indent=4))


conversation = _fetch(url="https://slack.com/api/users.conversations", desired_key="channels", types="im,mpim")
_save_to_file_as_json(data=conversation, file_path="./output/conversation.json")

channels = _fetch(url="https://slack.com/api/conversations.list", desired_key="channels", types="public_channel,private_channel")
_save_to_file_as_json(data=channels, file_path="./output/channels.json")

for channel in channels:
    channel_data = _fetch(url="https://slack.com/api/conversations.history", desired_key="messages", channel=channel.get('id'))
    _save_to_file_as_json(data=channel_data, file_path=f"./output/channels/{channel.get('name_normalized')}.json")
