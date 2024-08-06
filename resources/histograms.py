import cv2
import numpy as np
import sqlite3
from generator import get_image_paths
from embedding import get_embedding

def calculate_histogram(image, bins=(8, 8, 8)):
    """
    Calculate and normalize the color histogram of an image.
    
    Args:
        image (np.ndarray): RGB image.
        bins (tuple): Number of bins for each color channel.
    
    Returns:
        np.ndarray: Flattened and normalized histogram.
    """
    histogram = cv2.calcHist([image], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])
    cv2.normalize(histogram, histogram)
    return histogram.flatten()

def store_in_db(image_id, histogram, embedding, db_path):
    """
    Store the histogram and embedding in the database.
    
    Args:
        image_id (str): Unique identifier for the image.
        histogram (np.ndarray): Flattened histogram to store.
        embedding (np.ndarray): Embedding vector to store.
        db_path (str): Path to the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    hist_str = ','.join(map(str, histogram))
    emb_str = ','.join(map(str, embedding))
    c.execute("INSERT INTO histograms (image_id, histogram) VALUES (?, ?)", (image_id, hist_str))
    c.execute("INSERT INTO embeddings (image_id, embedding) VALUES (?, ?)", (image_id, emb_str))
    conn.commit()
    conn.close()

def preprocess_images(image_directory, db_path):
    """
    Preprocess images by calculating their histograms and embeddings, then storing them in the database.
    
    Args:
        image_directory (str): Path to the directory containing images.
        db_path (str): Path to the SQLite database.
    """
    for image_path in get_image_paths(image_directory):
        try:
            image_id = os.path.basename(image_path)  # Assuming the image ID is the filename
            image = cv2.imread(image_path)
            if image is None:
                continue
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            histogram = calculate_histogram(image_rgb)
            embedding = get_embedding(image_path)
            store_in_db(image_id, histogram, embedding, db_path)
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")

# Example usage:
# preprocess_images('path/to/images', 'path/to/database.db')