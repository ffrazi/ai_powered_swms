import os
import random
import string
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# Disable warnings for better readability
warnings.filterwarnings("ignore")

# Load pre-trained MobileNetV2 model + weights for image classification
model = MobileNetV2(weights='imagenet')

# Path to the directory where your images are stored
image_folder = 'dataset\train'  # Adjust this to your actual folder path

# Read the Excel sheet into a DataFrame
excel_data = pd.read_excel("image_data.xlsx")

# Create a dictionary to map image names to phone numbers
image_phone_dict = {}

# Populate the dictionary
for index, row in excel_data.iterrows():
    image_name = row['city']  # Assuming the Excel file has a column named 'Image'
    phone_number = row['phone no.']  # Assuming the Excel file has a column named 'Phone Number'
    
    # Check if the image file exists in the specified folder
    image_path = os.path.join(image_folder, image_name)
    if os.path.exists(image_path):
        image_phone_dict[image_name] = phone_number
    else:
        print(f"Image {image_name} not found in {image_folder}")

# Optionally, print the dictionary to confirm it works
print(image_phone_dict)

# Function to analyze images
def analyze_image(image_path):
    if not os.path.exists(image_path):
        return "Error: File does not exist."

    try:
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        preds = model.predict(img_array)
        label = decode_predictions(preds, top=1)[0][0][1]
        
        # Extract phone number from dictionary using image name
        image_name = os.path.basename(image_path)  # Get the file name from the path
        #phone_number = image_phone_dict.get(image_name, "Phone number not found")
        
        return f"I detected this image as: {label}"

    except Exception as e:
        return f"Error processing image: {str(e)}"

# Function for text-based responses
nltk.download('punkt')  # Punkt tokenizer for sentence splitting
nltk.download('wordnet')  # WordNet for lemmatizationo id

# Importing and reading the corpus
with open('swm.txt', 'r', errors='ignore') as f:
    raw_doc = f.read().lower()  # Converts text to lowercase

# Preprocessing for text normalization
lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = str.maketrans('', '', string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greeting function
GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREET_RESPONSES = ["hi", "hey", "nods", "hi there", "hello", "I am glad you are talking to me!"]

def greet(sentence):
    for word in sentence.split():
        if word.lower() in GREET_INPUTS:
            return random.choice(GREET_RESPONSES)
    return None

END_INPUTS = ("bye", "goodbye", "see you", "take care", "exit", "quit", "later")
END_RESPONSES = [
    "Goodbye! Have a great day!", 
    "See you soon!", 
    "Take care!", 
    "Bye! Stay safe!", 
    "It was nice talking to you. Bye!", 
    "Until next time!"
]

def end_conversation(sentence):
    for word in sentence.split():
        if word.lower() in END_INPUTS:
            return random.choice(END_RESPONSES)
    return None


# Text-based response generation
sent_tokens = nltk.sent_tokenize(raw_doc)  # Convert doc to list of sentences

def response(user_response):
    robo1_response = ''
    sent_tokens.append(user_response)
    
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english', token_pattern=None)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if req_tfidf == 0:
        robo1_response = "I am sorry! I don't understand you."
    else:
        robo1_response = sent_tokens[idx]
    
    sent_tokens.pop()  # Remove the user response after processing
    return robo1_response

# Main chatbot loop
#print("Hello! I am a Smart Waste Management Chatbot. Type 'bye' to exit. You can also upload an image for analysis.")

#while True:
    user_response = input("You: ").strip()

    if user_response.lower() == 'bye':
        print("Bot: Goodbye! Have a great day!")
        #break
    elif os.path.exists(user_response):  # Check if input is a valid file path (for image)
        print("Bot:", analyze_image(user_response))  # Image analysis
    elif greet(user_response) is not None:
        print("Bot:", greet(user_response))  # Textual greeting response
    else:
        print("Bot:", response(user_response))  # Text-based response generation