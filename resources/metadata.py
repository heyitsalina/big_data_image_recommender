import os
import sqlite3
from PIL import Image
import numba
import pickle
from tqdm import tqdm


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
