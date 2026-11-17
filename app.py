# import flask class
from flask import Flask, render_template, url_for
import os

# initialise flask application
app = Flask(__name__)

artists = [
    {
        "id": 1,
        "name": "Tame Impala",
        "slug": "tame-impala",
        "genre": "Psychedelic Rock",
        "description": "Australian psychedelic music project led by Kevin Parker.",
        "image": "images/artists/tame-impala/heroes/hero 1.jpeg",
        "portrait": "images/artists/tame-impala/portraits/portrait 1.jpeg"
    },
    {
        "id": 2,
        "name": "Mac DeMarco",
        "slug": "mac-demarco",
        "genre": "Indie Rock",
        "description": "Canadian singer-songwriter known for his laid-back indie sound.",
        "image": "images/artists/mac-demarco/heroes/hero 1.jpeg",
        "portrait": "images/artists/mac-demarco/portraits/portrait 1.jpeg"
    },
    {
        "id": 3,
        "name": "Sticky Fingers",
        "slug": "sticky-fingers",
        "genre": "Indie Rock / Reggae",
        "description": "Australian band known for blending indie rock, reggae and psychedelic influences.",
        "image": "images/artists/sticky-fingers/heroes/hero 1.jpeg",
        "portrait": "images/artists/sticky-fingers/portraits/portrait 1.jpeg"
    },
    {
        "id": 4,
        "name": "Frank Ocean",
        "slug": "frank-ocean",
        "genre": "Alternative R&B",
        "description": "American singer-songwriter known for his experimental R&B, emotional storytelling and atmospheric production.",
        "image": "images/artists/frank-ocean/heroes/hero 1.jpeg",
        "portrait": "images/artists/frank-ocean/portraits/portrait 1.jpeg"
    },
    {
        "id": 5,
        "name": "Khruangbin",
        "slug": "khruangbin",
        "genre": "Psychedelic Funk / Soul",
        "description": "American trio blending psychedelic funk, soul, dub and global musical influences.",
        "image": "images/artists/khruangbin/heroes/hero 1.jpeg",
        "portrait": "images/artists/khruangbin/portraits/portrait 1.jpeg"
    },
    {
        "id": 6,
        "name": "Men I Trust",
        "slug": "men-i-trust",
        "genre": "Dream Pop / Indie",
        "description": "Canadian indie band known for their dreamy melodies, smooth basslines and atmospheric sound.",
        "image": "images/artists/men-i-trust/heroes/hero 1.jpeg",
        "portrait": "images/artists/men-i-trust/portraits/portrait 1.jpeg"
    },
    {
        "id": 7,
        "name": "MF DOOM",
        "slug": "mf-doom",
        "genre": "Alternative Hip-Hop",
        "description": "British-American rapper and producer celebrated for his intricate wordplay, masked persona and underground hip-hop influence.",
        "image": "images/artists/mf-doom/heroes/hero 1.jpeg",
        "portrait": "images/artists/mf-doom/portraits/portrait 1.jpeg",
        "biography": (
            "MF DOOM was a British-American rapper and producer known for "
            "his intricate lyricism, comic-book-inspired identity and "
            "distinctive metal mask. Born Daniel Dumile, he became one "
            "of underground hip-hop's most influential figures. "
            "His music combined unusual samples, complex rhymes and "
            "an unmistakable sense of humour."
        ),
    },
    {
        "id": 8,
        "name": "PinkPantheress",
        "slug": "pink-pantheress",
        "genre": "UK Garage / Alternative Pop",
        "description": "British singer and producer known for blending UK garage, drum and bass, and nostalgic pop.",
        "image": "images/artists/pink-pantheress/heroes/hero 1.jpeg",
        "portrait": "images/artists/pink-pantheress/portraits/portrait 1.jpeg"
    },
    {
        "id": 9,
        "name": "Dope Lemon",
        "slug": "dope-lemon",
        "genre": "Psychedelic Rock / Indie Folk",
        "description": "Australian psychedelic music project led by Angus Stone, known for its laid-back grooves, dreamy melodies and mellow sound.",
        "image": "images/artists/dope-lemon/heroes/hero 1.jpeg",
        "portrait": "images/artists/dope-lemon/portraits/portrait 1.jpeg"
    },
    {
        "id": 10,
        "name": "Kaytranada",
        "slug": "kaytranada",
        "genre": "Electronic / House / Hip-Hop",
        "description": "Haitian-Canadian producer and DJ known for his distinctive blend of house, funk, hip-hop and R&B.",
        "image": "images/artists/kaytranada/heroes/hero 1.jpeg",
        "portrait": "images/artists/kaytranada/portraits/portrait 1.jpeg"
    },
    {
        "id": 11,
        "name": "Tyler, the Creator",
        "slug": "tyler-the-creator",
        "genre": "Alternative Hip-Hop / R&B",
        "description": "American rapper, producer and creative artist known for his genre-blending albums, distinctive production and visual style.",
        "image": "images/artists/tyler-the-creator/heroes/hero 1.jpeg",
        "portrait": "images/artists/tyler-the-creator/portraits/portrait 1.jpeg"
    },
    {
        "id": 12,
        "name": "Lorde",
        "slug": "lorde",
        "genre": "Alternative Pop / Art Pop",
        "description": "New Zealand singer-songwriter known for her distinctive vocals, introspective lyrics and atmospheric pop production.",
        "image": "images/artists/lorde/heroes/hero 1.jpeg",
        "portrait": "images/artists/lorde/portraits/portrait 1.jpeg"
    }
]

# home route for sending recieving requests, connects the homepage url
@app.route("/")
# define route function that will handle reququests
def home():
    # sends a response back to the browser
    return render_template("index.html", artists=artists)

@app.route("/artists")
def artists_page():
    return render_template("artists.html", artists=artists)

@app.route("/artists/<slug>")
def artist_page(slug):

    # Find the artist matching the URL slug
    for artist in artists:
        if artist["slug"] == slug:
            return render_template("artist.html", artist=artist)

    return "Artist not found", 404

# runs when everything before it is correct
if __name__ == "__main__":
  # starts the server
    app.run(debug=True, port=5001)