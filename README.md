# Slack exporter

## Setting up the project

### Requirements

* Python3
* pip

### Install

```bash
git clone https://github.com/PootisPenserHere/slack-exporter
cd slack-exporter
pip3 install -r requirements.txt
```

### Getting a token

* Head over to the [apps dashboard](https://api.slack.com/apps/) and create a new app.

  ![Apps dashboard](./docs/media/apps-dashboard.png)

![Create new app](./docs/media/create-app.png)

* Once created you'll be redirected to the apps settings, head over to the `Permissions` and scroll down to configure the app scopes.

  ![App settings](./docs/media/app-settings.png)

  ![App scopes](./docs/media/app-scopes.png)

The scopes should be granted to `User Token Scopes` and they're:

* [channels:history](https://api.slack.com/scopes/channels:history)
* [channels:read](https://api.slack.com/scopes/channels:read)
* [emoji:read](https://api.slack.com/scopes/emoji:read)
* [groups:history](https://api.slack.com/scopes/groups:history)
* [groups:read](https://api.slack.com/scopes/groups:read)
* [im:history](https://api.slack.com/scopes/im:history)
* [im:read](https://api.slack.com/scopes/im:read)
* [mpim:history](https://api.slack.com/scopes/mpim:history)
* [mpim:read](https://api.slack.com/scopes/mpim:read)
* [users:read](https://api.slack.com/scopes/users:read)

![App scopes set](./docs/media/app-scopes-set.png)

* With the scopes set scroll up and install the app in your work place, granting it permissions.

  ![Install app](./docs/media/install-app.png)

**NOTE** If the scopes are changed you'll need to reinstall the app.

* Finally you'll be given two tokens, copy the `OAuth Access Token` and create a file named `.env` at the root of the project and add the token the the field `SLACK_TOKEN`

  ![App tokens](./docs/media/app-tokens.png)

```text
# .env
SLACK_TOKEN=xoxp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Running the project

To execute the scrapper simply run

```bash
python3 app.py
```

The scrapped data will be placed in the `./output` directory

```text
$ tree output    
output
├── channels
│   ├── sample_channel_1.json
├── channels.json
├── conversation.json
├── conversations
│   ├── sample_conversation_1.json
├── emojis.json
├── users
│   ├── user_1.json
└── users.json

```

