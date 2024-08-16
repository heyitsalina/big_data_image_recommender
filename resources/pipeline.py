# File to create necessary tables and dataframes
from phashes import generate_hash
from generator import image_generator
from embedding import get_embedding
from histograms import calculate_histogram
from collections import defaultdict
import sqlite3
import numpy as np
import cv2
from PIL import Image
import os
import tqdm
import pickle


def upload_pickle(directory):
    
    
    try:
        with open("similarities.pkl", "rb") as f:
            similarities = pickle.load(f)
    except FileNotFoundError:
        similarities = defaultdict()
        similarities[0] = None

    # similarity_id = max(similarities.keys())
    img_gen = image_generator(directory)
    id = 0
    
    for img in tqdm.tqdm(img_gen, total=447584):
        id += 1
        
        # preprocess image for histogram and phash generation
        image_cv2 = cv2.imread(img)
        image_rgb = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
        histogram = calculate_histogram(np.array(image_rgb))
        phash = generate_hash(image_cv2)
        
        image_pil = Image.open(img).convert('RGB')
        embedding = get_embedding(image_pil, "cpu")
        
        
        similarities[id] = [histogram, embedding, phash]
        if id == 20:
            with open("similarities.pkl", "wb") as f:
                pickle.dump(similarities, f)
        
if __name__ == "__main__":
    directory_path = "D:\data\image_data"
    upload_pickle(directory_path)