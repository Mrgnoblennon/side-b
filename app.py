# import flask class
from flask import Flask

# initialise flask application
app = Flask(__name__)

# home route for sending recieving requests, connects the homepage url
@app.route("/")
# define route function that will handle reququests
def home():

  # sends a response back to the browser
  return "Welcome to the b-side home page."

# runs when everything before it is correct
if __name__ == "__main__":
  # starts the server
  app.run()