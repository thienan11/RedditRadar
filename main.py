import json
from flask import Flask, render_template, request

import praw
from prawcore.exceptions import NotFound, BadRequest

from dotenv import load_dotenv
import os

load_dotenv()

# Using render_template to render index.html template
# Using request to handle incoming http requests to our web app
# Using praw to authenticate with the Reddit API and to parse Reddit API's response

# Application instance of flask app
app = Flask(__name__, static_url_path='/static')

# Reddit API instance
reddit = praw.Reddit(
  client_id = os.getenv("REDDIT_CLIENT_ID"),
  client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
  user_agent = os.getenv("REDDIT_USER_AGENT"),
)

file = "reddit.json"


# Root for index page with flask
# Bind a URL to a python function that will handle request made to that URL
@app.route("/", methods=["GET", "POST"])

def index():
  subreddit_name = ''
  error_message = None
  data = []  # Initialize data as an empty list

  if request.method == "POST":
      subreddit_name = request.form["subreddit"].strip()

      if not subreddit_name:
        error_message = "Please enter a subreddit name."
      else:
        try:
          subreddit = reddit.subreddit(subreddit_name)
          new_data_list = []

          for post in subreddit.hot(limit=10):
              new_data_list.append({
                  "title": post.title,
                  "author": post.author.name,
                  "link": post.shortlink,
                  "body": post.selftext[:500] + "...",
              })

          with open(file, 'w') as f:
              json.dump(new_data_list, f, indent=2)

          with open(file, 'r') as f:
              data = json.load(f)

        except NotFound:
          error_message = f"The subreddit '{subreddit_name}' does not exist."
        except BadRequest as e:
          error_message = f"The subreddit '{subreddit_name}' is not valid."
        except Exception as e:
          # error_message = f"An unexpected error occurred: {str(e)}"
          error_message = f"Error occurred: Try again."

  return render_template("index.html", data=data, subreddit=subreddit_name, error_message=error_message)

if __name__ == "__main__":
  app.run(debug=True)