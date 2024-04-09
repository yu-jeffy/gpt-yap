from flask import Flask, render_template, request, jsonify, send_file
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
from openai import OpenAI
import tempfile
import requests
import json
import os

load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Initialize the speech recognizer
    recognizer = sr.Recognizer()
    
    # The audio file will be sent as part of the request
    audio_file = request.files['audio_data']
    
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        
    # Attempt to recognize the speech in the audio file
    try:
        text = recognizer.recognize_google(audio_data)
        return jsonify({'transcribed_text': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Speech recognition could not understand audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': 'Could not request results from speech recognition service; {0}'.format(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500



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
    # Assuming conversation_history is received as a JSON string of list of tuples
    conversation_history_json = request.form.get('conversation_history', '[]')
    conversation_history_tuples = json.loads(conversation_history_json)

    # Convert list of tuples into the format expected by OpenAI API
    conversation_history = [{"role": role, "content": content} for role, content in conversation_history_tuples]

    # Append the new user input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",  # Adjust the model name as necessary
            messages=conversation_history
        )

        # Extract the GPT response
        gpt_response = response.choices[0].message['content']

        # Update the conversation history tuples with the new response
        conversation_history_tuples.append(("assistant", gpt_response))

        # Convert the updated conversation history back to a JSON string
        updated_conversation_history_json = json.dumps(conversation_history_tuples)

        return jsonify({'gpt_response': gpt_response, 'updated_conversation_history': updated_conversation_history_json})
    except Exception as e:
        return jsonify({'error': 'Failed to get response from GPT API', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
