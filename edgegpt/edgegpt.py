from fastapi import FastAPI
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import asyncio, json

app = FastAPI()

@app.get("/gpt/{query}")
async def gpt(query: str):
    try:
        if query == "":
            return {"message": "No Prompt Provided"}

        response = await gptCall(query)
        return response
    except:
        return {"message": "Something went wrong"}

async def gptCall(query = ""):

    bot = await Chatbot.create()

    #prompt = "Your name is 'ELIO', Act as a productivity assistant and respond to this: " + query
    prompt = query

    print(prompt)

    response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
    
    await bot.close() 
    return response