def test_histogram_similarity():
    image1 = load_image('our_path_to_image1.jpg')
    image2 = load_image('our_path_to_image2.jpg')
    hist1 = calculate_histogram(image1)
    hist2 = calculate_histogram(image2)

    distance_cosine = compare_histograms_cosine(hist1, hist2)
    distance_intersection = compare_histograms_intersection(hist1, hist2)
    distance_emd = compare_histograms_emd(hist1, hist2)

    assert 0 <= distance_cosine <= 2, "Cosine distance should be between 0 and 2"
    assert 0 <= distance_intersection <= 1, "Intersection distance should be between 0 and 1"
    assert distance_emd >= 0, "EMD should be non-negative"

if __name__ == "__main__":
    db_path = 'images.db'
    
    # should be run only once in order to avoid error messages
    setup_database(db_path)

    # insert random images from our database for testing purposes
    # insert_image(db_path, 'our_path_to_image1.jpg')
    # insert_image(db_path, 'our_path_to_image2.jpg') usw...

    # run the test function
    test_histogram_similarity()

    # find similar images
    similar_images = find_similar_images('path/to/input_image.jpg', db_path, method='cosine')
    print(similar_images)
