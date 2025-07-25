from flask import Blueprint, request, jsonify
import os
import wave
import json
from vosk import Model, KaldiRecognizer

transcriber_bp = Blueprint("transcriber", __name__)

# Load Vosk model (expects model in 'vosk-model-small-en-us-0.15/')
VOSK_MODEL_PATH = "backend/models/vosk-model-small-en-us-0.15"
if not os.path.exists(VOSK_MODEL_PATH):
    raise RuntimeError("Vosk model not found. Please download and place it in 'backend/models/'.")

model = Model(VOSK_MODEL_PATH)

@transcriber_bp.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    if not audio_file.filename.endswith(".wav"):
        return jsonify({"error": "Only WAV files are supported"}), 400

    # Save file temporarily
    temp_path = "temp_audio.wav"
    audio_file.save(temp_path)

    # Open WAV file
    wf = wave.open(temp_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        wf.close()
        os.remove(temp_path)
        return jsonify({"error": "Audio must be WAV format (mono, 16-bit PCM)."}), 400

    rec = KaldiRecognizer(model, wf.getframerate())

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result()))

    # Final result
    results.append(json.loads(rec.FinalResult()))
    wf.close()
    os.remove(temp_path)

    # Combine transcriptions
    full_text = " ".join([res.get("text", "") for res in results])

    return jsonify({"transcription": full_text})
