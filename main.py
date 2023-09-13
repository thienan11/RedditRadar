import json
from flask import Flask, render_template, request
import praw

# Using render_template to render index.html template
# Using request to handle incoming http requests to our web app
# Using praw to authenticate with the Reddit API and to parse Reddit API's response

# Application instance of flask app
app = Flask(__name__)

# Reddit API instance
reddit = praw.Reddit(
  client_id="",
  client_secret="",
  user_agent="",
)

file = "reddit.json"


# Root for index page with flask
# Bind a URL to a python function that will handle request made to that URL
@app.route("/", methods=["GET", "POST"])

def index():
  pass
