# For writing a generator to read the images.
# Part of our first couple of milestones. 

# Alle files checken, die mit .png, .jpeg, .jpg, BILDERFORMATE --> als Funktion
# Alle diese Bilder in den Generator laden 
# Funktion, die die metadaten der Bilder auffängt 
# database sql 

import os
import sqlite3
from PIL import Image

# create the database in order to load the metadata through sqlite
conn = sqlite3.connect('image_metadata.db')
curs = conn.cursor()

# check if the folder 'image_metadata.db' does not exist
if not os.path.exists('image_metadata.db'):
    # Create the folder
    os.makedirs('image_metadata.db')


# create the table in which we load the metadata
# curs.execute('''
#     CREATE TABLE metadata (
#         id INTEGER PRIMARY KEY,
#         filename TEXT,
#         format TEXT,
#         mode TEXT,
#         width INTEGER,
#         height INTEGER,
#         size INTEGER
#     )
# ''')
# conn.commit()

def image_generator(directory):

    # generator that runs image files from our given directory as the parameter
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                yield os.path.join(root, file)

def get_image_metadata(image_path):

    # get the metadata of all the images we need through the image_path we have
    with Image.open(image_path) as img:
        metadata = {
            'filename': os.path.basename(image_path),
            'format': img.format,
            'mode': img.mode,
            'width': img.width,
            'height': img.height,
            'size': os.path.getsize(image_path)
        }
    return metadata

def save_metadata_to_db(metadata):

    # save the metadata from the images to the SQLite database.
    curs.execute('''
        INSERT INTO metadata (filename, format, mode, width, height, size)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (metadata['filename'], metadata['format'], metadata['mode'], 
         metadata['width'], metadata['height'], metadata['size']))
    conn.commit()

if __name__ == "__main__":
    # the directory (IMMER VON DER FESTPLATTE ABHÄNGIG UND DESSEN GERÄT)
    image_directory = 'F:\data\image_data'

    # generate image files and save their metadata to the database
    for image_path in image_generator(image_directory):
        metadata = get_image_metadata(image_path)
        save_metadata_to_db(metadata)

# close database connection in order to prevent any issues
conn.close()
