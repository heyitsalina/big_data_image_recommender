# Similarity 1 and 2 
# Similarity 1 - color based, Similarity 2 - Image Embedding and Similarity 3 - TO-DO !

import numpy as np
import sqlite3
from scipy.spatial import distance
from histograms import calculate_histogram, load_image


def get_histograms_from_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # HISTOGRAM DATABASE - TO DO !!!
    c.execute('SELECT image_id, histogram FROM histograms')
    histograms = [(row[0], np.fromstring(row[1], sep=',')) for row in c.fetchall()]
    conn.close()
    return histograms

def get_embeddings_from_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # EMBEDDINGS DATABASE - TO DO !!!
    c.execute('SELECT image_id, embedding FROM embeddings')
    embeddings = [(row[0], np.fromstring(row[1], sep=',')) for row in c.fetchall()]
    conn.close()
    return embeddings

# THE ACTUAL SIMILARITY SEARCH MEASURE FOR BOTH COLOR BASED AND IMAGE EMBEDDING
def find_similar_images(input_image_path, db_path, top_n=5, method='cosine', feature='histogram'):
    if feature == 'histogram':
        input_image = load_image(input_image_path)
        input_hist = calculate_histogram(input_image)
        histograms = get_histograms_from_db(db_path)
        similarities = []
        for image_id, hist in histograms:
            if method == 'cosine':
                dist = distance.cosine(input_hist, hist)
            elif method == 'intersection':
                dist = np.sum(np.minimum(input_hist, hist)) / np.sum(hist)
            elif method == 'emd':
                dist = np.sum(np.abs(np.cumsum(input_hist) - np.cumsum(hist)))
            similarities.append((image_id, dist))
        similarities.sort(key=lambda x: x[1])
    elif feature == 'embedding':
        input_emb = get_embedding(input_image_path)
        embeddings = get_embeddings_from_db(db_path)
        similarities = [(image_id, compare_embeddings_cosine(input_emb, emb)) for image_id, emb in embeddings]
        similarities.sort(key=lambda x: x[1])
    return [sim[0] for sim in similarities[:top_n]]

