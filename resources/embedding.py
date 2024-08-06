import numpy as np
import pandas as pd
import sqlite3
import tqdm
from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity

def euclidean_distance(v1, v2):
    return distance.euclidean(v1, v2)

def manhatten_distance(v1, v2):
    return distance.cityblock(v1, v2)

def cos_similarity(v1, v2):
    return cosine_similarity([v1], [v2])[0][0]


if __name__ == "__main__":
    # get the number of vectors 
    # create an empty matrix using numpy
    # iterate through every vector and compare it to every other vector
    print("Hello World!")
    conn = sqlite3.connect('big_data_image_recommender/image_metadata.db')
    df = pd.read_sql_query("SELECT * FROM metadata", conn)