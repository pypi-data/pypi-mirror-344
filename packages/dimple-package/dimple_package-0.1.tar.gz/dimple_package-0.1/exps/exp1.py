def run():
    print("Experiment 1: This is exp1")
"""
pip install nltk langdetect


import nltk
from langdetect import detect
from nltk.tokenize import word_tokenize

# Download tokenizer data for multiple languages
nltk.download('punkt')

def tokenize_multilingual(text):
    # Detect the language of the text
    language = detect(text)
    print(f"Detected language: {language}")

    # Tokenize the text based on the detected language
    tokens = word_tokenize(text, language=language)
    return tokens

# Example usage
text = input("Enter a sentence: ")
tokens = tokenize_multilingual(text)
print("Tokens:", tokens)


CHATBOT 

pip install nltk flask

import nltk
from nltk.chat.util import Chat, reflections
from flask import Flask, render_template, request

# Define chatbot responses
pairs = [
    (r"hi|hello", ["Hello!", "Hi there!"]),
    (r"how are you?", ["I'm doing well, thank you!"]),
    (r"quit", ["Goodbye!"]),
    (r"(.*)", ["I didn't understand that."])
]

chatbot = Chat(pairs, reflections)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['GET'])
def get_response():
    user_input = request.args.get('msg')
    return chatbot.respond(user_input)

if __name__ == "__main__":
    app.run(debug=True)




<!DOCTYPE html>
<html>
<head><title>Chatbot</title></head>
<body>
    <h2>Chatbot</h2>
    <div id="chatbox"></div>
    <input type="text" id="user_input" placeholder="Say something...">
    <button onclick="sendMessage()">Send</button>
    
    <script>
        function sendMessage() {
            var user_input = document.getElementById("user_input").value;
            fetch('/get?msg=' + user_input)
                .then(response => response.text())
                .then(data => {
                    document.getElementById("chatbox").innerHTML += "You: " + user_input + "<br>Bot: " + data + "<br>";
                    document.getElementById("user_input").value = "";
                });
        }
    </script>
</body>
</html>





python app.py


VOICEBOT

from flask import Flask, request, render_template_string
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import pyttsx3
from werkzeug.serving import run_simple

# Initialize Flask app
app = Flask(__name__)
recognizer = sr.Recognizer()

# Function to record audio using sounddevice
def record_audio(duration=5, samplerate=16000):
    print("Recording audio...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording to finish
    write("temp_audio.wav", samplerate, audio_data)  # Save the audio as a temporary WAV file

# Function to generate a response
def generate_response(user_input):
    if "hello" in user_input.lower():
        return "Hello I am Dr. Emmanuel Joy ! How can I assist you today?"
    elif "time" in user_input.lower():
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    elif "bye" in user_input.lower():
        return "Goodbye! Have a great day. See you in the division oF AI ML"
    elif "project" in user_input.lower():
        return "How can I guide you in your project"
    elif "ai" in user_input.lower():
        return "Artificial Intelligence is transforming the world. Glad you are in my class"
    else:
        return "I'm not sure how to respond to that."

# Function to convert text to speech
def speak(response):
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()

# Flask routes
@app.route("/")
def home():
    # HTML content as a string for Jupyter compatibility
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Voice Bot</title>
    </head>
    <body>
        <h1>Voice Bot</h1>
        <form action="/get_response" method="post">
            <button type="submit">Speak</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route("/get_response", methods=["POST"])
def get_response():
    # Record audio using sounddevice
    record_audio(duration=5)

    # Recognize speech from the recorded audio
    try:
        with sr.AudioFile("temp_audio.wav") as source:
            audio = recognizer.record(source)
            user_input = recognizer.recognize_google(audio)
            print("User Input:", user_input)

            # Generate and return the bot's response
            response = generate_response(user_input)
            speak(response)
            return f"User said: {user_input}<br>Bot Response: {response}"
    except Exception as e: n2    
        return f"Error: {e}"

# Run Flask using werkzeug's run_simple for Jupyter compatibility
if __name__ == "__main__":
    run_simple("localhost", 5000, app)



"""