import os
import re

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from hbcbot import commands


app = Flask(__name__)

brewfather_share_re = re.compile(r'https://share.brewfather.app/(\w+)')


@app.route('/healthcheck')
def healthcheck():
    return 'ok'


# event handler / server
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret,
                                         endpoint="/slack/events",
                                         server=app)

# web API for sending messages
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(token=slack_bot_token)


def print_help(args):
    return('commands: .abv')


command_map = {
    'abv': commands.calc_abv,
    'help': print_help,
}


# handler for all messages
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    print('event hit: %s' % event_data)
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get('subtype') is not None:
        # nfi what this means, but it's in the example. probably threads
        return
    msg_text = message.get('text')
    channel = message["channel"]
    if not msg_text:
        # wtf?
        return

    if msg_text.startswith('.'):
        # we have a bot command
        cmd, *args = msg_text.lstrip('.').split()
        cmd = command_map.get(cmd)
        if not cmd:
            return
        response = cmd(args)
        slack_client.chat_postMessage(channel=channel, text=response)

    elif 'share.brewfather.app' in msg_text:
        bfid = brewfather_share_re.findall(msg_text)
        # TODO(jroll) deal with multiple URLs
        new_url = 'https://web.brewfather.app/#/share/%s' % bfid[0]
        response = 'for people on work internets: %s' % new_url
        slack_client.chat_postMessage(channel=channel, text=response)


# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))