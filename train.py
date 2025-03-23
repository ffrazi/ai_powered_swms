import os
import numpy as np
import pickle
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input

# Load the pre-trained MobileNetV2 model (Feature Extractor)
model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# Folder paths and feature file locations
image_folder = 'dataset/train'  # Folder containing images to be processed
feature_file = 'image_features.pkl'  # File where features will be saved

# Check if image folder exists
if not os.path.exists(image_folder):
    print(f"Error: The folder '{image_folder}' does not exist!")
else:
    print(f"Image folder '{image_folder}' found.")

# Function to extract features from an image
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

# Start processing the images
dataset_features = {}

# Walk through the directory and subdirectories
for root, dirs, files in os.walk(image_folder):
    print(f"Scanning directory: {root}")

    # Process each file in the current directory
    for img_name in files:
        img_path = os.path.join(root, img_name)

        # Ensure it's a valid image file (with proper extensions)
        if os.path.isfile(img_path) and img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            print(f"Processing image: {img_name}")

            # Extract features
            features = extract_features(img_path)
            
            if features is not None:
                dataset_features[img_name] = features
            else:
                print(f"Skipping {img_name} due to feature extraction error.")
        else:
            print(f"Skipping {img_name} (not a valid image file).")

# Check if features were extracted
if dataset_features:
    print(f"Extracted features for {len(dataset_features)} images.")
    # Save features to pickle file
    with open(feature_file, 'wb') as f:
        pickle.dump(dataset_features, f)
    print(f"Features successfully saved to {feature_file}.")
else:
    print("No features were extracted. Check for issues with the images or extraction.")

# Debug: Output the first few entries in dataset_features
print(f"First few extracted features: {list(dataset_features.keys())[:5]}")
