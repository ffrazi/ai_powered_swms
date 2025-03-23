import os
from text import analyze_image, response, greet, end_conversation  # Importing the functions from text.py
from gps import get_current_location, get_closest_phone_number  # Import GPS functions
from images import load_features, extract_features, get_closest_match  # Import image-related functions

# Main chatbot loop
print("Hello! I am a Smart Waste Management Chatbot. Type 'bye' to exit.")
print("If you'd like to check your location, just type 'location'.")
print("You can also type 'image' to upload an image for analysis.")

while True:
    user_response = input("You: ").strip().lower()

    if end_conversation(user_response):  # Check if the user wants to end the chat
        print("Bot:", end_conversation(user_response))
        break
    elif user_response == 'location':  # Check if the user wants their location
        current_location = get_current_location()  # Call the GPS function to get the current location
        print("Bot: Your current location is:", current_location)
        phone_number, distance = get_closest_phone_number(current_location, "image_data.xlsx")
        # Now, only print the phone number and distance here
        print(f"Bot: Closest phone number: {phone_number}, Distance: {distance} km")
    
    elif user_response == 'image':  # If the user wants to upload an image for analysis
        # Ask for the image path
        img_path = input("Please provide the image path: ").strip()
        if os.path.exists(img_path):  # Check if the file exists
            result = analyze_image(img_path)  # Call analyze_image function from images.py
            print("Bot: Image Analysis Result:", result)
            # Move phone number and distance printing outside the image analysis logic
            current_location = get_current_location()  # Call the GPS function to get the current location
            print("Bot: Your current location is:", current_location)
            phone_number, distance = get_closest_phone_number(current_location, "image_data.xlsx")
            # Now, only print the phone number and distance here
            print(f"Bot: Closest phone number: {phone_number}, Distance: {distance} km")
        else:
            print("Bot: Error: The image file does not exist. Please provide a valid image path.")
    
    elif os.path.exists(user_response):  # If the input is a valid image path
        print("Bot: Analyzing the image...")  # Process the image
        result = analyze_image(user_response)  # Image analysis
        print("Bot:", result)
    
    elif user_response == 'query image':  # If the user wants to query the image dataset
        input_image = input("Enter the path of the image to query: ").strip()
        dataset_features = load_features()  # Load features from the dataset
        if os.path.exists(input_image):  # Check if the image file exists
            match, similarity = get_closest_match(input_image, dataset_features)
            if match:
                print(f"Bot: Closest Image Match: {match} (Similarity: {similarity:.2f})")
            else:
                print("Bot: No matching image found.")
        else:
            print("Bot: Error: The image file does not exist. Please provide a valid image path.")
    
    elif greet(user_response) is not None:  # Check if it's a greeting
        print("Bot:", greet(user_response))  # Textual greeting response
    
    else:  # Default response for unrecognized inputs
        print("Bot:", response(user_response))  # Text-based response generation
