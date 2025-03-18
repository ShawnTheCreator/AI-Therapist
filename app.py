from flask import Flask, render_template, request, jsonify
from pathlib import Path
from bot import TherapistBot
import boto3
import os
from dotenv import load_dotenv
import logging

# Load environment variables from Render environment settings
load_dotenv()

app = Flask(__name__)

# Ensure FLASK_SECRET_KEY is set
app.secret_key = os.getenv("FLASK_SECRET_KEY")
if not app.secret_key:
    raise ValueError("FLASK_SECRET_KEY is not set")

# Create static directories (Render has an ephemeral file system)
Path("static/css").mkdir(parents=True, exist_ok=True)
Path("static/images").mkdir(parents=True, exist_ok=True)

# Initialize AI bot
bot = TherapistBot()

# AWS Polly Client
polly_client = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name='us-west-2'
).client('polly')

VOICES = {'unisex': 'Joanna', 'female': 'Salli', 'male': 'Matthew'}

# Logging Configuration
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        logging.debug("Received data: %s", data)

        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided', 'therapy_response': None}), 400

        user_input = data['text']
        ai_response = bot.get_response(user_input)
        logging.debug("AI response: %s", ai_response)

        return jsonify({'therapy_response': ai_response, 'status': 'success'})
    except Exception as e:
        logging.error("Error: %s", str(e))
        return jsonify({'error': str(e), 'therapy_response': 'An error occurred.', 'status': 'error'}), 500

@app.route('/generate_speech', methods=['POST'])
def generate_speech():
    try:
        data = request.json
        text = data.get('text')
        voice_type = data.get('voice_type', 'unisex')

        if voice_type not in VOICES:
            return jsonify({"error": "Invalid voice type"}), 400

        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=VOICES[voice_type]
        )

        audio_file = f"static/output_{voice_type}.mp3"
        with open(audio_file, 'wb') as f:
            f.write(response['AudioStream'].read())

        logging.debug("Audio file saved at: %s", audio_file)
        return jsonify({"file": audio_file})
    except Exception as e:
        logging.error("Error in /generate_speech: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/mood-trends')
def mood_trends():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('Settings.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/health")
def health():
    return "OK", 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get assigned port
    app.run(host='0.0.0.0', port=port, debug=False)  # Disable debug in production
