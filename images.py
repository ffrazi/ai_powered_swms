import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input

# Load the pre-trained MobileNetV2 model (Feature Extractor)
model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# Folder paths and feature file locations
image_folder = 'dataset/train'  # Folder containing images to be processed
feature_file = 'image_features.pkl'  # File where features are stored

# Load features from the pickle file
def load_features():
    if os.path.exists(feature_file):
        with open(feature_file, 'rb') as f:
            dataset_features = pickle.load(f)
            print(f"Features successfully loaded from {feature_file}.")
            return dataset_features
    else:
        print(f"Error: The file '{feature_file}' does not exist!")
        return {}

# Function to extract features from an image (used for querying)
def extract_features(img_path):
    try:
        print(f"Loading image from {img_path}...")
        img = image.load_img(img_path, target_size=(224, 224))  # Resize image to match model input
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = preprocess_input(img_array)  # Preprocess for MobileNetV2
        features = model.predict(img_array)  # Extract features
        print(f"Features extracted for {img_path} with shape: {features.shape}")
        return features
    except Exception as e:
        print(f"Error extracting features for {img_path}: {e}")
        return None

# Function to find the closest match for an input image
def get_closest_match(input_image_path, dataset_features):
    input_features = extract_features(input_image_path)

    if input_features is None:
        return None

    best_match = None
    highest_similarity = -1

    for img_name, features in dataset_features.items():
        similarity = cosine_similarity(input_features, features)[0][0]
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = img_name

    return best_match, highest_similarity

# Main function to test the image query
def main():
    # Load the dataset features
    dataset_features = load_features()

    if not dataset_features:
        return  # No features to process

    # User input: Image path
    input_image = input("Enter the path of the image to query: ").strip()

    if os.path.exists(input_image):
        match, similarity = get_closest_match(input_image, dataset_features)

        if match:
            print(f"Closest Image Match: {match} (Similarity: {similarity:.2f})")
        else:
            print("No matching image found.")
    else:
        print("Error: Image file not found.")

if __name__ == "__main__":
    main()
