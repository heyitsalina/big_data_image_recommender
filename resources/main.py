# This is supposed to be the file that everything runs through.
# We don't need to figure this out right away, but we also shouldn't work on this last minute.

import argparse
import cv2
import matplotlib.pyplot as plt
from similarity_search import find_similar_images

def show_images(image_paths, input_image_path):
    input_image = cv2.cvtColor(cv2.imread(input_image_path), cv2.COLOR_BGR2RGB)
    images = [input_image]
    
    for path in image_paths:
        image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        images.append(image)
    
    titles = ["Input Image"] + [f"Similar Image {i+1}" for i in range(len(image_paths))]
    
    plt.figure(figsize=(15, 5))
    for i, img in enumerate(images):
        plt.subplot(1, len(images), i+1)
        plt.imshow(img)
        plt.title(titles[i])
        plt.axis('off')
    
    plt.show()

def main(input_image_path, db_path, top_n, method, feature):
    similar_images = find_similar_images(input_image_path, db_path, top_n, method, feature)
    print(f"The top {top_n} similar images to {input_image_path} are:")
    for img in similar_images:
        print(img)
    show_images(similar_images, input_image_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image Recommender System')
    parser.add_argument('input_image', type=str, help='Path to the input image')
    parser.add_argument('db_path', type=str, help='Path to the database')
    parser.add_argument('--top_n', type=int, default=5, help='Number of top similar images to retrieve')
    parser.add_argument('--method', type=str, default='cosine', choices=['cosine', 'intersection', 'emd'], help='Similarity method to use')
    parser.add_argument('--feature', type=str, default='histogram', choices=['histogram', 'embedding'], help='Feature to use for similarity search')
    
    args = parser.parse_args()
    main(args.input_image, args.db_path, args.top_n, args.method, args.feature)