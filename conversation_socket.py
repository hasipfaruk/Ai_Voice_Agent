# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse
# from fastapi import BackgroundTasks
# import asyncio
# import random
# from pydub import AudioSegment
# from pydub.playback import play

# from my_bot import ConversationManager, TextToSpeech, get_transcript

# app = FastAPI()

# # Create instance of ConversationManager
# manager = ConversationManager()

# @app.get("/")
# async def get():
#     return HTMLResponse("""
#         <html>
#             <body>
#                 <h1>Conversation API</h1>
#                 <p>WebSocket connection is required to interact with the service.</p>
#             </body>
#         </html>
#     """)

# audio_files = [
#     'wait.mp3',
#     'patiant.mp3',
#     'checking.mp3',
#     'getting.mp3',
#     'hold.mp3',
#     'find.mp3'
# ]

# @app.websocket("/ws/conversation")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     def handle_full_sentence(full_sentence):
#         # This method will handle the full sentence from the user and store it
#         asyncio.create_task(websocket.send_text(full_sentence))

#     # Start the main conversation loop
#     try:
#         while True:
#             selected_audio = random.choice(audio_files)
#             audio_segment = AudioSegment.from_file(selected_audio)

#             # Listen to user input and process
#             await get_transcript(handle_full_sentence, audio_segment)

#             if "goodbye" in manager.transcription_response.lower():
#                 await websocket.send_text("Goodbye! Ending conversation.")
#                 break

#             llm_response = manager.llm.process(manager.transcription_response)
            
#             # Play the audio and then speak the response
#             play(audio_segment)
            
#             tts = TextToSpeech()
#             # Use asyncio.to_thread to run the synchronous speak() method asynchronously
#             await asyncio.to_thread(tts.speak, llm_response)

#             # Reset the transcription response for the next loop
#             manager.transcription_response = ""
#             await websocket.send_text(llm_response)

#     except WebSocketDisconnect:
#         print("Client disconnected")

# @app.post("/start_conversation/")
# async def start_conversation(background_tasks: BackgroundTasks):
#     background_tasks.add_task(manager.main)
#     return {"message": "Conversation started in the background!"}

# # Running the API using Uvicorn
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import asyncio
# import random
# from pydub import AudioSegment
# from pydub.playback import play
# import tempfile

# from my_bot import ConversationManager, TextToSpeech, get_transcript

# app = FastAPI()

# # Create instance of ConversationManager
# manager = ConversationManager()

# audio_files = [
#     'wait.mp3',
#     'patiant.mp3',
#     'checking.mp3',
#     'getting.mp3',
#     'hold.mp3',
#     'find.mp3'
# ]

# @app.websocket("/ws/conversation")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
    
#     try:
#         while True:
#             # Receive raw audio data from the client
#             audio_data = await websocket.receive_bytes()

#             # Save the received audio data to a temporary file
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
#                 temp_audio.write(audio_data)
#                 temp_audio_path = temp_audio.name  # Get file path

#             # Process the transcription
#             full_sentence = await get_transcript(temp_audio_path)

#             if "goodbye" in full_sentence.lower():
#                 await websocket.send_text("Goodbye! Ending conversation.")
#                 break

#             # Generate response from LLM
#             llm_response = manager.llm.process(full_sentence)

#             # Send text response first
#             await websocket.send_text(llm_response)

#             # Select a random pre-recorded audio file
#             selected_audio = random.choice(audio_files)
#             audio_segment = AudioSegment.from_file(selected_audio)

#             # Play the pre-recorded audio asynchronously
#             asyncio.create_task(play_audio_async(audio_segment))

#             # Convert LLM response to speech
#             tts = TextToSpeech()
#             speech_audio_path = tts.speak(llm_response)

#             # Send generated speech audio back to the client
#             with open(speech_audio_path, "rb") as audio_file:
#                 await websocket.send_bytes(audio_file.read())

#     except WebSocketDisconnect:
#         print("Client disconnected")

# async def play_audio_async(audio_segment):
#     """Play audio asynchronously to avoid blocking the event loop."""
#     await asyncio.to_thread(play, audio_segment)


# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import asyncio
# import random
# from pydub import AudioSegment
# from pydub.playback import play
# import tempfile
# import uvicorn

# from my_bot import ConversationManager, TextToSpeech, get_transcript

# app = FastAPI()

# # Create instance of ConversationManager
# manager = ConversationManager()

# audio_files = [
#     'wait.mp3',
#     'patiant.mp3',
#     'checking.mp3',
#     'getting.mp3',
#     'hold.mp3',
#     'find.mp3'
# ]

# # Define handle_full_sentence function outside of websocket_endpoint
# def handle_full_sentence(full_sentence, websocket):
#     # This method will handle the full sentence from the user and send it over WebSocket
#     asyncio.create_task(websocket.send_text(full_sentence))

# @app.websocket("/ws/conversation")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     # Start the main conversation loop
#     try:
#         while True:
#             selected_audio = random.choice(audio_files)
#             audio_segment = AudioSegment.from_file(selected_audio)

#             # Listen to user input and process
#             await get_transcript(lambda full_sentence: handle_full_sentence(full_sentence, websocket), audio_segment)

#             if "goodbye" in manager.transcription_response.lower():
#                 await websocket.send_text("Goodbye! Ending conversation.")
#                 break

#             llm_response = manager.llm.process(manager.transcription_response)
            
#             # Play the audio and then speak the response
#             play(audio_segment)
            
#             tts = TextToSpeech()
#             # Use asyncio.to_thread to run the synchronous speak() method asynchronously
#             await asyncio.to_thread(tts.speak, llm_response)

#             # Reset the transcription response for the next loop
#             manager.transcription_response = ""
#             await websocket.send_text(llm_response)

#     except WebSocketDisconnect:
#         print("Client disconnected")

# async def play_audio_async(audio_segment):
#     """Play audio asynchronously to avoid blocking the event loop."""
#     await asyncio.to_thread(play, audio_segment)

# # Start the FastAPI server with Uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)



import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import random
from pydub import AudioSegment
from io import BytesIO
from my_bot import ConversationManager, TextToSpeech, get_transcript  # Custom bot methods

app = FastAPI()

manager = ConversationManager()

audio_files = [
    'wait.mp3',
    'patient.mp3',
    'checking.mp3',
    'getting.mp3',
    'hold.mp3',
    'find.mp3'
]

# Helper function to handle transcription and send response back
async def handle_full_sentence(full_sentence, websocket):
    await websocket.send_text(full_sentence)

@app.websocket("/ws/conversation")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            # Receive the audio chunk from the client
            audio_chunk = await websocket.receive_bytes()

            # Process the audio and convert it to text (speech-to-text)
            audio_segment = AudioSegment.from_file(BytesIO(audio_chunk), format="wav")
            transcription = await get_transcript(lambda full_sentence: handle_full_sentence(full_sentence, websocket), audio_segment)

            if "goodbye" in transcription.lower():
                await websocket.send_text("Goodbye! Ending conversation.")
                break

            # Get the bot's response to the transcription
            llm_response = manager.llm.process(transcription)

            # Convert the response text to speech (text-to-speech)
            tts = TextToSpeech()
            bot_audio = await asyncio.to_thread(tts.speak, llm_response)

            # Send the bot's speech audio back to the client
            await websocket.send_bytes(bot_audio)

    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
