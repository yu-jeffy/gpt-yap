from flask import Flask, render_template, request, jsonify, send_file
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Transcription logic as previously implemented
    pass

@app.route('/synthesize', methods=['POST'])
def synthesize_speech():
    text = request.form['text']
    tts = gTTS(text=text, lang='en')
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    tts.save(temp_file.name)
    
    # Return the audio file
    return send_file(temp_file.name, as_attachment=True, attachment_filename='response.mp3')

@app.route('/ask-gpt', methods=['POST'])
def ask_gpt():
    user_input = request.form['user_input']
    conversation_history = request.form.get('conversation_history', '')
    
# Using the correct syntax and endpoint from gptexample.py
gpt_api_url = 'https://api.openai.com/v4/completions'
headers = {
    'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
    'Content-Type': 'application/json',
}

payload = {
    'model': 'gpt-4-turbo-preview',  # Adjust the model name as necessary
    'messages': conversation_history + [{"role": "user", "content": user_input}]
}

response = requests.post(gpt_api_url, json=payload, headers=headers)

if response.status_code == 200:
    gpt_response = response.json()['choices'][0]['message']['content']
    return jsonify({'gpt_response': gpt_response})
else:
    return jsonify({'error': 'Failed to get response from GPT API'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
