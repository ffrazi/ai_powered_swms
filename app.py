from flask import Flask, render_template, request, jsonify
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

# Initialize the Flask app
app = Flask(__name__)

# Disable warnings for better readability
warnings.filterwarnings("ignore")

# Load pre-trained MobileNetV2 model + weights for image classification
model = MobileNetV2(weights='imagenet')

# Path to the directory where your images are stored
image_folder = 'dataset\\train'  # Adjust this to your actual folder path

# Read the Excel sheet into a DataFrame
excel_data = pd.read_excel("image_data.xlsx")

# Create a dictionary to map image names to phone numbers
image_phone_dict = {}

# Populate the dictionary
for index, row in excel_data.iterrows():
    image_name = row['city']  # Assuming the Excel file has a column named 'city'
    phone_number = row['phone no.']  # Assuming the Excel file has a column named 'Phone Number'
    
    # Check if the image file exists in the specified folder
    image_path = os.path.join(image_folder, image_name)
    if os.path.exists(image_path):
        image_phone_dict[image_name] = phone_number
    else:
        print(f"Image {image_name} not found in {image_folder}")

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

        return f"I detected this image as: {label}"

    except Exception as e:
        return f"Error processing image: {str(e)}"

# Text-based response generation
nltk.download('punkt')  # Punkt tokenizer for sentence splitting
nltk.download('wordnet')  # WordNet for lemmatization

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

# Routes for rendering templates
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# New API route to handle chatbot functionality
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message').strip()  # Get the user's input

    # Check if the user wants to end the conversation
    if end_conversation(user_message):
        return jsonify({'response': end_conversation(user_message)})

    # Handle location request (if implemented in the future)
    if user_message == 'location':
        current_location = get_current_location()
        phone_number, distance = get_closest_phone_number(current_location, "image_data.xlsx")
        return jsonify({
            'response': f"Your current location is: {current_location}\nClosest phone number: {phone_number}, Distance: {distance} km"
        })

    # Handle image upload request
    elif user_message == 'image':
        return jsonify({'response': 'Please provide the image path for analysis.'})

    # Handle image query request
    elif user_message == 'query image':
        return jsonify({'response': 'Enter the path of the image to query.'})

    # Handle image analysis request if the input is a valid image path
    elif os.path.exists(user_message):  # If the input is an image path
        result = analyze_image(user_message)
        return jsonify({'response': result})

    # Default greeting handling
    elif greet(user_message) is not None:
        return jsonify({'response': greet(user_message)})

    # Default response for unrecognized inputs
    else:
        return jsonify({'response': response(user_message)})

if __name__ == '__main__':
    app.run(debug=True)
