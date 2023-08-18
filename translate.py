import speech_recognition as sr
from langdetect import detect
from googletrans import Translator
from gtts import gTTS
import os

# Creating a recognizer object and a text-to-speech object
r = sr.Recognizer()

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
            translator = Translator()
            translation = translator.translate(text, dest='en').text
            # Speak the translated text
            tts = gTTS(text=translation, lang="en")
            tts.save("translated_speech.mp3")
            os.system("start translated_speech.mp3")

        # Translate speech to French if detected language is English
        elif input_language == "en":
            translator = Translator()
            translation = translator.translate(text, dest='fr').text
            print("Translated to French:", translation)
            # Speak the translated text
            tts = gTTS(text=translation, lang="fr")
            tts.save("translated_speech.mp3")
            os.system("start translated_speech.mp3")

        else:
            print("Unsupported language")
    except sr.UnknownValueError as e:
        print(f"Google Speech Recognition could not understand audio (speak like a human not like an animal): {e}")
