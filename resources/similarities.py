# Similarity 1 and 2 
# Similarity 1 - color based and Similarity 2 - xxx

import cv2
import numpy as np
import sqlite3
from scipy.spatial import distance

Class color_similarity():

    def load_image(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb

    def calculate_histogram(image, bins=(8, 8, 8)):
        histogram = cv2.calcHist([image], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])
        cv2.normalize(histogram, histogram)
        return histogram.flatten()

    def compare_histograms(hist1, hist2, method='cosine'):
        return distance.cdist([hist1], [hist2], method=method)[0][0]

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
            dist = compare_histograms(input_hist, hist, method=method)
            similarities.append((image_path, dist))

        similarities.sort(key=lambda x: x[1])
        return [sim[0] for sim in similarities[:top_n]]

    # Unit test for histogram similarity
    def test_histogram_similarity():
        image1 = load_image('path/to/image1.jpg')
        image2 = load_image('path/to/image2.jpg')
        hist1 = calculate_histogram(image1)
        hist2 = calculate_histogram(image2)
        distance_cosine = compare_histograms(hist1, hist2, method='cosine')

        assert 0 <= distance_cosine <= 2, "Cosine distance should be between 0 and 2"

    if __name__ == "__main__":
        # Run the test
        test_histogram_similarity()

        # Find similar images
        similar_images = find_similar_images('path/to/input_image.jpg', 'images.db')
        print(similar_images)
