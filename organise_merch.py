
from pathlib import Path
import shutil

# location of all artist folders
base_path = Path(__file__).resolve().parent / "static/images/artists"

# check every artist folder
for artist in base_path.iterdir():

    # skip placeholders and non-artist folders
    if not artist.is_dir() or artist.name == "placeholders":
        continue

    merch_folder = artist / "merch"
    tshirt_folder = merch_folder / "t-shirts"

    # skip artists without a merch folder
    if not merch_folder.exists():
        continue

    # create t-shirts folder if missing
    tshirt_folder.mkdir(parents=True, exist_ok=True)

    # find merch 1 images
    for image in merch_folder.glob("merch 1.*"):

        # keep the original file extension
        new_name = f"t-shirt 1{image.suffix.lower()}"
        destination = tshirt_folder / new_name

        # avoid overwriting existing images
        if destination.exists():
            print(f"Skipped: {destination} already exists")
            continue

        # move and rename the image
        shutil.move(str(image), str(destination))

        print(
            f"Moved: {artist.name}/merch/{image.name} "
            f"-> {artist.name}/merch/t-shirts/{new_name}"
        )

print("\nFinished organising T-shirt images!")
