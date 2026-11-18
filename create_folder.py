
import os

# all SIDE B. artists
artists = [
    "tame-impala",
    "mac-demarco",
    "sticky-fingers",
    "frank-ocean",
    "khruangbin",
    "men-i-trust",
    "mf-doom",
    "pink-pantheress",
    "dope-lemon",
    "kaytranada",
    "tyler-the-creator",
    "lorde"
]

# folders for each artist
folders = [
    "heroes",
    "portraits",
    "gallery",
    "merch/t-shirts",
    "merch/hoodies",
    "merch/hats",
    "merch/vinyl",
    "merch/artwork",
    "merch/tote-bags",
    "merch/sweatshirts",
    "merch/accessories"
]

# location of artist images
base_path = os.path.join("static", "images", "artists")

# create folders for every artist
for artist in artists:
    for folder in folders:
        path = os.path.join(base_path, artist, folder)

        os.makedirs(path, exist_ok=True)

        print(f"Created: {path}")

# create placeholder folder
placeholder_path = os.path.join(base_path, "placeholders")
os.makedirs(placeholder_path, exist_ok=True)

print("\nAll SIDE B. folders are ready!")
