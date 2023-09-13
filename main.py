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
  client_id="ZmVW-vgxRrbwQslpzs4sWw",
  client_secret="LEA7IgS_0ATF5wwjg41BovxWrNCtWQ",
  user_agent="reRadar by u/TinAnonymous",
)

file = "reddit.json"


# Root for index page with flask
# Bind a URL to a python function that will handle request made to that URL
@app.route("/", methods=["GET", "POST"])

def index():
  subreddit_name = "reddit"
  if request.method == "POST":
    subreddit_name = request.form["subreddit"]
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

  return render_template("index.html", data=data, subreddit=subreddit)

if __name__ == "__main__":
  app.run(debug=True)