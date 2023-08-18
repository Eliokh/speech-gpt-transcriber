#this is my full enhanced code from google cloud console API(but the problem is that is paid(require billing))

import speech_recognition as sr
from langdetect import detect
from google.cloud import translate_v2 as translate
from gtts import gTTS
import os
import pandas



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'translatorcloud.json'

# Creating a recognizer object and a text-to-speech object
r = sr.Recognizer()

def translate_text(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

while True:
    # Use the default mic as the audio source
    with sr.Microphone() as source:
        print("Start Speaking...")
        # Adjusting the ambient noise level
        r.adjust_for_ambient_noise(source)
        # Listen for audio inputs from the user
        audio = r.listen(source)

    try:
        # Recognize speech using Google Web Speech API
        text = r.recognize_google(audio)
        input_language = detect(text)

        # Translate speech to English if detected language is French
        if input_language == "fr":
            translation = translate_text(text, 'en')
            # Speak the translated text
            tts = gTTS(text=translation, lang="en")
            tts.save("translated_speech.mp3")
            os.system("start translated_speech.mp3")

        # Translate speech to French if detected language is English
        elif input_language == "en":
            translation = translate_text(text, 'fr')
            print("Translated to French:", translation)
            # Speak the translated text
            tts = gTTS(text=translation, lang="fr")
            tts.save("translated_speech.mp3")
            os.system("start translated_speech.mp3")

        else:
            print("Unsupported language")
    except sr.UnknownValueError as e:
        print(f"Google Speech Recognition could not understand audio (speak like a human not like an animal): {e}")
