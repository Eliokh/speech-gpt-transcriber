# from flask import Flask, request, render_template
# from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
# import speech_recognition as sr
# import asyncio
# import os
# from gtts import gTTS

# app = Flask(__name__)

# async def gptCall(query=""):
#     bot = await Chatbot.create()

#     response = await bot.ask(
#         prompt=query,
#         conversation_style=ConversationStyle.creative,
#         simplify_response=True
#     )

#     await bot.close()
#     return response

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         # Transcribe speech to text
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             print("Start Speaking...")
#             r.adjust_for_ambient_noise(source)
#             audio = r.listen(source)

#         try:
#             text = r.recognize_google(audio)
#             print("Transcribed Text:", text)

#             # Call the GPT API with transcribed text
#             gpt_response = asyncio.run(gptCall(text))

#             # Get the GPT response text
#             gpt_text_response = gpt_response['simplified']

#             # Save GPT response as an audio file
#             tts = gTTS(text=gpt_text_response, lang="en")
#             tts.save("static/gpt_response.mp3")

#             return render_template(
#                 "index.html",
#                 transcribed_text=text,
#                 gpt_response_text=gpt_text_response
#             )
#         except sr.UnknownValueError as e:
#             return "Speech recognition error"

#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(host="localhost", port=8091)


from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import speech_recognition as sr
import asyncio
from gtts import gTTS

async def gptCall(query=""):
    bot = await Chatbot.create()

    response = await bot.ask(
        prompt=query,
        conversation_style=ConversationStyle.creative,
        simplify_response=True
    )

    await bot.close()
    return response

def test_app():
    # Transcribe speech to text
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Start Speaking...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("Transcribed Text:", text)

        # Call the GPT API with transcribed text
        gpt_response = asyncio.run(gptCall(text))

        # Get the GPT response text
        gpt_text_response = gpt_response['simplified']

        # Save GPT response as an audio file
        tts = gTTS(text=gpt_text_response, lang="en")
        tts.save("gpt_response.mp3")

        print("GPT Response Text:", gpt_text_response)
    except sr.UnknownValueError as e:
        print("Speech recognition error")

if __name__ == "__main__":
    test_app()

