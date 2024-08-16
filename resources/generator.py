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
import pickle
from tqdm import tqdm


# @numba.jit() --> numba is more appropriate for numerical operations, less for filepath and string operations

# TODO: Add starting point architecture to resume generating from the last id in the database

def load_checkpoint(checkpoint_file):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'rb') as f:
            return pickle.load(f) # pickle file for checkpoint loading
    return None

def save_checkpoint(checkpoint_file, last_processed_file):
    with open(checkpoint_file, 'wb') as f:
        pickle.dump(last_processed_file, f) # saving of the checkpoint loading-pickle file 

def count_images(directory):
    # function to count the total number of image files in the given directors (needed for tqdm progress bar)
    total_images = 0
    for root, _, files in os.walk(directory):
        total_images += len([file for file in files if file.lower().endswith(('png', 'jpg', 'jpeg'))])
    return total_images

def image_generator(directory, checkpoint_file='checkpoint.pkl'):
    # the main generator - loads the last processed file from the checkpoint
    last_processed_file = load_checkpoint(checkpoint_file)
    resume_processing = False if last_processed_file is None else True

    total_images = count_images(directory)  # counts total images for the progress bar
    pbar = tqdm(total=total_images, desc="Processing images")  # initialize progress bar

    if last_processed_file:
        # finds the index of the last processed file to set the correct progress bar position
        pbar.n = sum([1 for root, _, files in os.walk(directory) for file in files 
                      if os.path.join(root, file).lower().endswith(('png', 'jpg', 'jpeg')) and 
                      os.path.join(root, file) <= last_processed_file])
        pbar.refresh()

    for root, _, files in os.walk(directory):
        files.sort()  # sort files to ensure consistent ordering

        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                file_path = os.path.join(root, file)

                if resume_processing:
                    if file_path == last_processed_file:
                        resume_processing = False  # found the last processed file, resume processing
                    continue

                # Load the image with PIL
                image = Image.open(file_path)

                # Save the current file as a checkpoint
                save_checkpoint(checkpoint_file, file_path)

                yield image  
                
                pbar.update(1)  # Update the progress bar

    pbar.close()  # Close the progress bar

    # Once all files are processed, remove the checkpoint file
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)


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

def save_image_to_db(image_path):

    # use the generated image_path to get the images' binary data
    with open(image_path, "rb") as f:
        data = f.read()

    # save the images' filepath and binary data to the SQLite database.
    curs.execute(
        """
        INSERT INTO image (filename, image)
        VALUES (?, ?)
    """,
        (os.path.basename(image_path), data),
    )
    conn.commit()


# delete all unnecessary data in the table
def reset_table(table):
    curs.execute(f"DELETE FROM {table}")
    conn.commit()


""" def get_img_rgb(image_path):
    
    img = Image.open(image_path)
    
    img.convert("RGB")
    width, height = img.size
    
    red = []
    green = []
    blue = []
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x,y))
            red.append(r)
            green.append(g)
            blue.append(b)
            curs.execute("INSERT INTO metadata (red, green, blue) VALUES (?, ?, ?)",
                (red, green, blue),
            )
            conn.commit() """

# implement a loop to feed 1000 images into the metadata database
# TODO: Maybe we could just load both at the same time instead of doing either or
# TODO: Add functionality to add histograms and embeddings to the database
def insert_into_db(table, batchsize=1000):
    pbar = tqdm.tqdm(total=batchsize)
    counter = 0

    # Choose which table you want to add data to. Put "metadata" for the metadata table and "image" for the image table.
    if table == "metadata":
        for image_path in image_generator(image_directory):
            metadata = get_image_metadata(image_path)
            save_metadata_to_db(metadata)
            pbar.update(1)
            counter += 1
            if counter == batchsize:
                break

        pbar.close()

    elif table == "image":
        for image_path in image_generator(image_directory):
            save_image_to_db(image_path)
            pbar.update(1)
            counter += 1
            if counter == batchsize:
                break

        pbar.close()

if __name__ == "__main__":
    
    # create the database in order to load the metadata through sqlite
    conn = sqlite3.connect('image_metadata.db')
    curs = conn.cursor()

    """ # check if the folder 'image_metadata.db' does not exist
    if not os.path.exists('image_metadata.db'):
        # Create the folder
        os.makedirs('image_metadata.db') """
    
    # the directory (IMMER VON DER FESTPLATTE ABHÄNGIG UND DESSEN GERÄT)
    image_directory = 'D:\data\image_data'

    reset_table("metadata")
    insert_into_db("metadata")
    
    # close database connection in order to prevent any issues
    curs.close()
    conn.close() 
    


