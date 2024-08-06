# Similarity 1 and 2 
# Similarity 1 - color based, Similarity 2 - Image Embedding and Similarity 3 - TO-DO !

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

# def compare_histograms_intersection(hist1, hist2):
#     minima = np.minimum(hist1, hist2)
#     return np.true_divide(np.sum(minima), np.sum(hist2))

# def compare_histograms_emd(hist1, hist2):
#     hist1_cdf = np.cumsum(hist1)
#     hist2_cdf = np.cumsum(hist2)
#     return np.sum(np.abs(hist1_cdf - hist2_cdf))

def get_histograms_from_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT image_id, histogram FROM histograms')
    histograms = {row[0]: np.array(list(map(float, row[1].split(',')))) for row in c.fetchall()}
    conn.close()
    return histograms

def get_embeddings_from_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT image_id, embedding FROM embeddings')
    embeddings = {row[0]: np.array(list(map(float, row[1].split(',')))) for row in c.fetchall()}
    conn.close()
    return embeddings

# Similarity search function
def find_similar_images(input_image_path, db_path, top_n=5, method='cosine', feature='histogram'):
    if feature == 'histogram':
        input_image = load_image(input_image_path)
        input_hist = calculate_histogram(input_image)
        histograms = get_histograms_from_db(db_path)

        similarities = []
        for image_id, hist in histograms.items():
            if method == 'cosine':
                dist = compare_histograms_cosine(input_hist, hist)
            elif method == 'intersection':
                dist = compare_histograms_intersection(input_hist, hist)
            elif method == 'emd':
                dist = compare_histograms_emd(input_hist, hist)
            else:
                raise ValueError(f"Unknown method: {method}")
            similarities.append((image_id, dist))

    elif feature == 'embedding':
        from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
        from tensorflow.keras.preprocessing import image
        from tensorflow.keras.models import Model
        
        model = VGG16(weights='imagenet', include_top=False)
        embedding_model = Model(inputs=model.input, outputs=model.layers[-1].output)
        
        img = image.load_img(input_image_path, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        input_embedding = embedding_model.predict(img_data).flatten()
        
        embeddings = get_embeddings_from_db(db_path)

        similarities = []
        for image_id, embedding in embeddings.items():
            if method == 'cosine':
                dist = distance.cosine(input_embedding, embedding)
            elif method == 'euclidean':
                dist = distance.euclidean(input_embedding, embedding)
            else:
                raise ValueError(f"Unknown method: {method}")
            similarities.append((image_id, dist))

    else:
        raise ValueError(f"Unknown feature: {feature}")

    similarities.sort(key=lambda x: x[1])
    return [sim[0] for sim in similarities[:top_n]]
