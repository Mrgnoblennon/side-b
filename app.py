# import flask class
from flask import Flask, render_template, url_for
import random, os

def random_artist_image(artist, category):
    folder = os.path.join(
        app.static_folder, "images", "artists", artist, category
    )

    images = [
        file for file in os.listdir(folder)
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]

    if not images:
        return None

    selected = random.choice(images)

    return url_for(
        "static",
        filename=f"images/artists/{artist}/{category}/{selected}"
    )

# initialise flask application
app = Flask(__name__)

# home route for sending recieving requests, connects the homepage url
@app.route("/")
# define route function that will handle reququests
def home():

  artists = [
    {
        "name": "Tame Impala",
        "portrait": random_artist_image("tame-impala", "portraits")
    },
    {
        "name": "Mac DeMarco",
        "portrait": random_artist_image("mac-demarco", "portraits")
    },
    {
        "name": "Sticky Fingers",
        "portrait": random_artist_image("sticky-fingers", "portraits")
    }
  ]
  
  hero_image = random_artist_image("tame-impala", "heroes")


  # sends a response back to the browser
  return render_template("index.html", artists=artists, hero_image=hero_image)

# runs when everything before it is correct
if __name__ == "__main__":
  # starts the server
    app.run(debug=True, port=5001)