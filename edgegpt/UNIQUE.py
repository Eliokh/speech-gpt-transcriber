from fastapi import FastAPI, Form
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import speech_recognition as sr
import asyncio
import os
from gtts import gTTS


app = FastAPI()

async def gptCall(query=""):
    bot = await Chatbot.create()

    response = await bot.ask(
        prompt=query,
        conversation_style=ConversationStyle.creative,
        simplify_response=True
    )

    await bot.close()
    return response

@app.post("/talk")
async def talk_and_listen(query: str = Form(...)):
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
        gpt_response = await gptCall(text)

        # Get the GPT response text
        gpt_text_response = gpt_response['simplified']

        # Save GPT response as an audio file
        tts = gTTS(text=gpt_text_response, lang="en")
        tts.save("gpt_response.mp3")
        os.system("start gpt_response.mp3")

        return {
            "transcribed_text": text,
            "gpt_response_text": gpt_text_response
        }
    except sr.UnknownValueError as e:
        return {"error": "Speech recognition error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8091)
