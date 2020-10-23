from dotenv import load_dotenv
import requests, os, json

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

    new_cursor = output['response_metadata']['next_cursor']
    if new_cursor:
        return output.get('channels') + _fetch(url, new_cursor)

    return output.get('channels')


channels = _fetch(url="https://slack.com/api/conversations.list")
with open("./output/channels.json", 'w') as channels_file:
    channels_file.write(json.dumps(channels, sort_keys=False, indent=4))
