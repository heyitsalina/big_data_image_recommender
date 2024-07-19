# For writing a generator to read the images.
# Part of our first couple of milestones.

# Alle files checken, die mit .png, .jpeg, .jpg, BILDERFORMATE --> als Funktion
# Alle diese Bilder in den Generator laden
# Funktion, die die metadaten der Bilder auffängt
# database sql

import os
import sqlite3
from PIL import Image
import numba
import tqdm


# @numba.jit() --> numba is more appropriate for numerical operations, less for filepath and string operations
def image_generator(directory):
    # generator that runs image files from our given directory as the parameter
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(("png", "jpg", "jpeg")):
                yield os.path.join(root, file)


def get_image_metadata(image_path):

    # get the metadata of all the images we need through the image_path we have
    with Image.open(image_path) as img:
        metadata = {
            "filename": os.path.basename(image_path),
            "format": img.format,
            "mode": img.mode,
            "width": img.width,
            "height": img.height,
            "size": os.path.getsize(image_path),
        }
    return metadata


def save_metadata_to_db(metadata):

    # save the metadata from the images to the SQLite database.
    curs.execute(
        """
        INSERT INTO metadata (filename, format, mode, width, height, size)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            metadata["filename"],
            metadata["format"],
            metadata["mode"],
            metadata["width"],
            metadata["height"],
            metadata["size"],
        ),
    )
    conn.commit()


def save_image_to_db(image):

    # save the metadata from the images to the SQLite database.
    curs.execute(
        """
        INSERT INTO image (filename, image)
        VALUES (?, ?)
    """,
        (),
    )
    conn.commit()


# delete all unnecessary data in the table
def reset_table(table):
    curs.execute(f"DELETE FROM {table}")
    conn.commit()


# DONE: implement a loop to feed 1000 images into the metadata database
def insert_into_db(batchsize=1000):
    pbar = tqdm.tqdm(total=batchsize)
    counter = 0
    for image_path in image_generator(image_directory):
        metadata = get_image_metadata(image_path)
        save_metadata_to_db(metadata)
        pbar.update(1)
        counter += 1
        if counter == batchsize:
            break

    pbar.close()


if __name__ == "__main__":

    # create the database in order to load the metadata through sqlite
    conn = sqlite3.connect("image_metadata.db")
    curs = conn.cursor()

    # check if the folder 'image_metadata.db' does not exist
    if not os.path.exists("image_metadata.db"):
        # Create the folder
        os.makedirs("image_metadata.db")

    # the directory (IMMER VON DER FESTPLATTE ABHÄNGIG UND DESSEN GERÄT)
    image_directory = "D:\data\image_data"

    # reset_table("metadata")
    # insert_into_db()

    # close database connection in order to prevent any issues
    curs.close()
    conn.close()

    # TODO: Make a database with just the images and put the same 1000 images there
