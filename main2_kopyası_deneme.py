import os
import sounddevice as sd
from flask import Flask, render_template, request, jsonify
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

app = Flask(__name__)
duration = 5  # kayıt saniyeleri
sample_rate = 44100
recording_state = {
    "is_recording": False,
    "audio_data": None,
    "last_result": ""
}
language_codes = {
    'es': 'İspanyolca',
    'ru': 'Rusça',
    'en': 'İngilizce',
    'tr': 'Türkçe',
    'fr': 'Fransızca',
    'de': 'Almanca',
    'it': 'İtalyanca',
    'pt': 'Portekizce',
    'ja': 'Japonca',
    'zh-cn': 'Çince'
}
kelime_listesi_en = {
    "kolay": [
        {"tr": "Elma", "en": "Apple"},
        {"tr": "Kedi", "en": "Cat"},
        {"tr": "Su", "en": "Water"},
        {"tr": "Masa", "en": "Table"},
        {"tr": "Mavi", "en": "Blue"},
        {"tr": "Kapı", "en": "Door"},
        {"tr": "Süt", "en": "Milk"},
        {"tr": "Mutlu", "en": "Happy"},
        {"tr": "Kitap", "en": "Book"},
        {"tr": "Okul", "en": "School"}
    ],
    "orta": [
        {"tr": "Bahçe", "en": "Garden"},
        {"tr": "Hava Durumu", "en": "Weather"},
        {"tr": "Macera", "en": "Adventure"},
        {"tr": "Tehlikeli", "en": "Dangerous"},
        {"tr": "Yarın", "en": "Tomorrow"},
        {"tr": "Kütüphane", "en": "Library"},
        {"tr": "Sincap", "en": "Squirrel"},
        {"tr": "Başarılı", "en": "Successful"},
        {"tr": "Çarşamba", "en": "Wednesday"},
        {"tr": "Dil", "en": "Language"}
    ],
    "zor": [
        {"tr": "Albay", "en": "Colonel"},
        {"tr": "Kuyruk", "en": "Queue"},
        {"tr": "Vicdan", "en": "Conscience"},
        {"tr": "Kaos", "en": "Chaos"},
        {"tr": "Program", "en": "Schedule"},
        {"tr": "Girişimci", "en": "Entrepreneur"},
        {"tr": "Psikoloji", "en": "Psychology"},
        {"tr": "Koro", "en": "Choir"},
        {"tr": "Kapsamlı", "en": "Thorough"},
        {"tr": "Hiyerarşi", "en": "Hierarchy"}
    ]
}
# Google Speech Recognition dil kodları
SPEECH_LANG_MAP = {
    'en': 'en-US',
    'es': 'es-ES',
    'fr': 'fr-FR',
    'de': 'de-DE',
    'it': 'it-IT',
    'pt': 'pt-PT',
    'ru': 'ru-RU',
    'ja': 'ja-JP',
    'zh-cn': 'zh-CN',
    'tr': 'tr-TR'
}
@app.route("/")
def index():
    return render_template("index_2.html")
"""@app.route("/")` → biri `localhost:5000` adresine girince bu fonksiyon çalışır
render_template` → `templates/` klasöründeki HTML'i bulur ve gönderir
"""

@app.route("/api/start-recording", methods=["POST"])
def start_recording():
    if recording_state["is_recording"]:
        return jsonify({"error": "Zaten kayıt yapılıyor"}), 400
    
    recording_state["is_recording"] = True
    recording_state["audio_data"] = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    return jsonify({"status": "recording", "duration": duration})
@app.route("/api/stop-recording", methods=["POST"])
def stop_recording():
    if not recording_state["is_recording"]:
        return jsonify({"error": "Kayıt yok"}), 400

    # HTML'den dil kodunu al
    data = request.get_json()
    user_lang = data.get("lang", "en")
    lang_code = SPEECH_LANG_MAP.get(user_lang, "en-US")

    sd.wait()
    recording_state["is_recording"] = False

    wav.write("output.wav", sample_rate, recording_state["audio_data"])
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language=lang_code)  # Dinamik dil
        recording_state["last_result"] = text
        return jsonify({"status": "done", "heard": text})
    except sr.UnknownValueError:
        return jsonify({"status": "error", "heard": "", "message": "Ses anlaşılamadı"})
    except sr.RequestError as e:
        return jsonify({"status": "error", "heard": "", "message": f"API hatası: {e}"})@app.route("/api/check-text", methods=["POST"])

@app.route("/api/check-text", methods=["POST"])
def check_text():
    data = request.get_json()
    user_text = data.get("text", "").strip()
    correct_answer = data.get("correct", "").strip()
    
    if not user_text or not correct_answer:
        return jsonify({"error": "Eksik veri"}), 400
    
    return jsonify({
        "status": "done",
        "heard": user_text
    })

def check_text():
    data = request.get_json()
    user_text = data.get("text", "").strip()
    correct_answer = data.get("correct", "").strip()
    
    if not user_text or not correct_answer:
        return jsonify({"error": "Eksik veri"}), 400
    
    return jsonify({
        "status": "done",
        "heard": user_text
    })

if __name__ == "__main__":
    app.run(debug=True)
