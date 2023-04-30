import os
import re
import json
import threading
import requests
import hmac
import hashlib

from flask import Flask, json, request
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter

from hbcbot import commands


app = Flask(__name__)


@app.route("/healthcheck")
def healthcheck():
    return "ok"


# event handler / server
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(
    slack_signing_secret, endpoint="/slack/events", server=app
)

# web API for sending messages
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(token=slack_bot_token)

if os.environ["SLACKBOT_DEBUG"] is not None:
    debug = True
else:
    debug = False


def print_help(args):
    return "commands: .abv .brix .hydrometer .untappd"


command_map = {
    "abv": commands.calc_abv,
    "brix": commands.brix_sg,
    "hydrometer": commands.hydro_adj,
    "help": print_help,
    "untappd": commands.untappd,
}


# handler for all messages
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    if debug:
        print("event hit: %s" % event_data)
    if message.get("subtype") is not None:
        # nfi what this means, but it's in the example. probably threads
        return
    msg_text = message.get("text")
    channel = message["channel"]
    if not msg_text:
        # wtf?
        return

    if msg_text.startswith("."):
        # we have a bot command
        cmd, *args = msg_text.lstrip(".").split()
        cmd = command_map.get(cmd.lower())
        if debug:
            print("command hit: %s", cmd)
        if not cmd:
            return
        response = cmd(args)
        if isinstance(response, str):
            slack_client.chat_postMessage(channel=channel, text=response)
        else:
            slack_client.chat_postMessage(channel=channel, blocks=json.dumps(response))

    if re.search(r"\b69\b", msg_text):
        if debug:
            print("69 hit: %s", msg_text)
        slack_client.reactions_add(
            channel=channel, name="nice", timestamp=message["ts"]
        )


@slack_events_adapter.on("member_joined_channel")
def handle_join(event_data):
    message = event_data["event"]
    channel = message["channel"]

    if channel == "C0FKR5YDT":  # this is the ID for #general
        # if channel == "C8TTK8Y58":  # this is the ID for #bot_stuff
        response = (
            """HBC welcome <@%s>
https://i.imgur.com/mHznIY8.png"""
            % message["user"]
        )
        slack_client.chat_postMessage(channel=channel, text=response, unfurl_links=True)


# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


def validate_slack_caller(request,signing_secret) -> bool:
    request_data = request.get_data()
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    signature_basestring = 'v0:' + timestamp + ':' + request_data.decode('utf-8')
    req_signature = 'v0=' + hmac.new(signing_secret.encode('utf-8'), signature_basestring.encode('utf-8'), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(req_signature, signature):
        return False
        if debug:
            print("Bad signing sig on untappd request")
    else:
        return True


# Slash commands
def untappd_worker(response_url,query):
    response = commands.untappd(query)
    if isinstance(response, str):
        message = { "text": response }
    else:
        message = { "blocks": response, "response_type": "in_channel" }
    res = requests.post(response_url, json=message)

@app.route('/untappd', methods=['POST'])
def untappd_response():
    if not validate_slack_caller(request,slack_signing_secret):
        return '', 403
    slack_request = request.form
    response_url = slack_request["response_url"]
    query = slack_request["text"]
    x = threading.Thread(
            target=untappd_worker,
            args=(response_url,query,)
        )
    x.start()
    return "Okay hoss, let me check on that with untappd for you"

