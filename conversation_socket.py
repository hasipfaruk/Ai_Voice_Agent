from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi import BackgroundTasks
import asyncio
import random
from pydub import AudioSegment
from pydub.playback import play

from my_bot import ConversationManager, TextToSpeech, get_transcript

app = FastAPI()

# Create instance of ConversationManager
manager = ConversationManager()

@app.get("/")
async def get():
    return HTMLResponse("""
        <html>
            <body>
                <h1>Conversation API</h1>
                <p>WebSocket connection is required to interact with the service.</p>
            </body>
        </html>
    """)

audio_files = [
    'wait.mp3',
    'patiant.mp3',
    'checking.mp3',
    'getting.mp3',
    'hold.mp3',
    'find.mp3'
]

@app.websocket("/ws/conversation")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    def handle_full_sentence(full_sentence):
        # This method will handle the full sentence from the user and store it
        asyncio.create_task(websocket.send_text(full_sentence))

    # Start the main conversation loop
    try:
        while True:
            selected_audio = random.choice(audio_files)
            audio_segment = AudioSegment.from_file(selected_audio)

            # Listen to user input and process
            await get_transcript(handle_full_sentence, audio_segment)

            if "goodbye" in manager.transcription_response.lower():
                await websocket.send_text("Goodbye! Ending conversation.")
                break

            llm_response = manager.llm.process(manager.transcription_response)
            
            # Play the audio and then speak the response
            play(audio_segment)
            
            tts = TextToSpeech()
            # Use asyncio.to_thread to run the synchronous speak() method asynchronously
            await asyncio.to_thread(tts.speak, llm_response)

            # Reset the transcription response for the next loop
            manager.transcription_response = ""
            await websocket.send_text(llm_response)

    except WebSocketDisconnect:
        print("Client disconnected")

@app.post("/start_conversation/")
async def start_conversation(background_tasks: BackgroundTasks):
    background_tasks.add_task(manager.main)
    return {"message": "Conversation started in the background!"}

# Running the API using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
