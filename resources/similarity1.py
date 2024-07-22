# Similarity 1 and 2 
# Similarity 1 - color based and Similarity 2 - xxx

import cv2
import numpy as np
import sqlite3
from scipy.spatial import distance

def load_image(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb

def calculate_histogram(image, bins=(8, 8, 8)):
    histogram = cv2.calcHist([image], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])
    cv2.normalize(histogram, histogram)
    return histogram.flatten()

def compare_histograms_cosine(hist1, hist2):
    return distance.cosine(hist1, hist2)

def compare_histograms_intersection(hist1, hist2):
    minima = np.minimum(hist1, hist2)
    return np.true_divide(np.sum(minima), np.sum(hist2))

def compare_histograms_emd(hist1, hist2):
    hist1_cdf = np.cumsum(hist1)
    hist2_cdf = np.cumsum(hist2)
    return np.sum(np.abs(hist1_cdf - hist2_cdf))

def get_image_paths_from_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT path FROM images')
    image_paths = [row[0] for row in c.fetchall()]
    conn.close()
    return image_paths

def find_similar_images(input_image_path, db_path, top_n=5, method='cosine'):
    input_image = load_image(input_image_path)
    input_hist = calculate_histogram(input_image)

    image_paths = get_image_paths_from_db(db_path)
    similarities = []
    for image_path in image_paths:
        image = load_image(image_path)
        hist = calculate_histogram(image)
        
        if method == 'cosine':
            dist = compare_histograms_cosine(input_hist, hist)
        elif method == 'intersection':
            dist = compare_histograms_intersection(input_hist, hist)
        elif method == 'emd':
            dist = compare_histograms_emd(input_hist, hist)
        else:
            raise ValueError(f"Unknown method: Please restart this process.")

        similarities.append((image_path, dist))

    similarities.sort(key=lambda x: x[1])
    return [sim[0] for sim in similarities[:top_n]]
