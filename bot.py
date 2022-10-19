import slack
import json

from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

from tdxreq import *

AUTH_TOKEN = "[removed]"
SECRET = "[removed]"

app = Flask(__name__);
adap = SlackEventAdapter(SECRET, "/events", app)
client = slack.WebClient(token=AUTH_TOKEN)

BOT_ID = client.api_call("auth.test")["user_id"]

@app.route("/cmd/test", methods=["POST"])
def testCmd():
	data = request.form
	print(data)
	channel = "#testing"# "#" + data["channel_name"]

	# ID of the thread (the replies to chats)
	thread_id = client.chat_postMessage(channel=channel, text="Creating ticket...").data["ts"]

	status = newTicket(data)

	client.chat_postMessage(channel=channel, text=status, thread_ts=thread_id)
	return Response(), 200



# As long as this file is run as main, start web server
if __name__ == "__main__":
	app.run(debug=True, port=4000)
