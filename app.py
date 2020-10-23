import errno
import json
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv(".env")


def _fetch(url: str, desired_key: str = None, next_cursor: str = None, **kwargs) -> list:
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

    results = output.get(desired_key) if desired_key else output
    if new_cursor and desired_key:
        return results + _fetch(url, desired_key, new_cursor, **kwargs)

    return results


def _save_to_file_as_json(data, file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(file_path, 'w') as file:
        file.write(json.dumps(data, sort_keys=False, indent=4))


emojis = _fetch(url="https://slack.com/api/emoji.list", desired_key="emoji")
_save_to_file_as_json(data=emojis, file_path="./output/emojis.json")

users = _fetch(url="https://slack.com/api/users.list", desired_key="members")
_save_to_file_as_json(data=users, file_path="./output/users.json")

for user in users:
    user_data = _fetch(url="https://slack.com/api/users.info", user=user.get('id'))
    _save_to_file_as_json(data=user_data, file_path=f"./output/users/{user.get('id')}.json")

conversations = _fetch(url="https://slack.com/api/users.conversations", desired_key="channels", types="im,mpim")
_save_to_file_as_json(data=conversations, file_path="./output/conversation.json")

for conversation in conversations:
    conversation_data = _fetch(url="https://slack.com/api/conversations.history", desired_key="messages", channel=conversation.get('id'))

    # Conversations with more than two participants have a normalized string name in the same
    # of regular one on one direct messages they do not have this field so we tag them
    # with the id of the conversation
    name = conversation.get('name_normalized') if "name_normalized" in conversation else conversation.get('id')
    _save_to_file_as_json(data=conversation_data, file_path=f"./output/conversations/{name}.json")

channels = _fetch(url="https://slack.com/api/conversations.list", desired_key="channels", types="public_channel,private_channel")
_save_to_file_as_json(data=channels, file_path="./output/channels.json")

for channel in channels:
    channel_data = _fetch(url="https://slack.com/api/conversations.history", desired_key="messages", channel=channel.get('id'))
    _save_to_file_as_json(data=channel_data, file_path=f"./output/channels/{channel.get('name_normalized')}.json")
