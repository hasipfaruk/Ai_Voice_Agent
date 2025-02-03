from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import random
from pydub import AudioSegment
from pydub.playback import play

from my_bot import ConversationManager, TextToSpeech, get_transcript

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
            selected_audio = random.choice(audio_files)
            audio_segment = AudioSegment.from_file(selected_audio)

            # Listen to user input and process
            await get_transcript(handle_full_sentence, audio_segment)

            if "goodbye" in transcription.lower():
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)