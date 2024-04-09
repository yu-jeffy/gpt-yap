import speech_recognition as sr
from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Global variable to control the recording state
is_recording = False

def record_audio(duration=5):
    global is_recording
    is_recording = True
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust the recognizer sensitivity to ambient noise
        recognizer.adjust_for_ambient_noise(source)
        print("Recording started")
        audio = recognizer.listen(source, timeout=duration)
        print("Recording stopped")
    is_recording = False
    # Save the audio file or process it here

@app.route('/start-recording', methods=['POST'])
def start_recording():
    global is_recording
    if not is_recording:
        # Start recording in a separate thread to avoid blocking
        duration = request.form.get('duration', 5)
        threading.Thread(target=record_audio, args=(duration,)).start()
        return jsonify({'message': 'Recording started'}), 200
    else:
        return jsonify({'message': 'Recording is already in progress'}), 400

@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    global is_recording
    if is_recording:
        is_recording = False
        return jsonify({'message': 'Recording stopped'}), 200
    else:
        return jsonify({'message': 'No recording in progress'}), 400

if __name__ == '__main__':
    app.run(debug=True)