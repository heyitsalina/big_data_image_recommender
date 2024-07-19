# Similarity 1 and 2 
# Similarity 1 - color based and Similarity 2 - xxx

import cv2
import numpy as np
import sqlite3
from scipy.spatial import distance

class ColorSimilarity:
    def __init__(self, db_path):
        self.db_path = db_path

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY,
                path TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def insert_image(self, image_path, metadata=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO images (path, metadata) VALUES (?, ?)', (image_path, metadata))
        conn.commit()
        conn.close()

    def get_image_paths_from_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT path FROM images')
        image_paths = [row[0] for row in c.fetchall()]
        conn.close()
        return image_paths

    def load_image(self, image_path):
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image_rgb

    def calculate_histogram(self, image, bins=(8, 8, 8)):
        histogram = cv2.calcHist([image], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])
        cv2.normalize(histogram, histogram)
        return histogram.flatten()

    def compare_histograms(self, hist1, hist2, method='cosine'):
        return distance.cdist([hist1], [hist2], method=method)[0][0]

    def find_similar_images(self, input_image_path, top_n=5, method='cosine'):
        input_image = self.load_image(input_image_path)
        input_hist = self.calculate_histogram(input_image)

        image_paths = self.get_image_paths_from_db()
        similarities = []
        for image_path in image_paths:
            image = self.load_image(image_path)
            hist = self.calculate_histogram(image)
            dist = self.compare_histograms(input_hist, hist, method=method)
            similarities.append((image_path, dist))

        similarities.sort(key=lambda x: x[1])
        return [sim[0] for sim in similarities[:top_n]]

    def test_histogram_similarity(self):
        image1 = self.load_image('path/to/image1.jpg')
        image2 = self.load_image('path/to/image2.jpg')
        hist1 = self.calculate_histogram(image1)
        hist2 = self.calculate_histogram(image2)
        distance_cosine = self.compare_histograms(hist1, hist2, method='cosine')

        assert 0 <= distance_cosine <= 2, "Cosine distance should be between 0 and 2"

if __name__ == "__main__":
    cs = ColorSimilarity('images.db')
    cs.setup_database()

    # Run the test
    cs.test_histogram_similarity()

    # Insert some images (this should be done separately as part of your database setup)
    # cs.insert_image('path/to/image1.jpg')
    # cs.insert_image('path/to/image2.jpg')

    # Find similar images
    similar_images = cs.find_similar_images('path/to/input_image.jpg')
    print(similar_images)
