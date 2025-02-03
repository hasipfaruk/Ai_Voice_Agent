# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import random
# from pydub import AudioSegment
# from pydub.playback import play

# from my_bot import ConversationManager, TextToSpeech, get_transcript

# app = FastAPI()

# manager = ConversationManager()

# audio_files = [
#     'wait.mp3',
#     'patiant.mp3',
#     'checking.mp3',
#     'getting.mp3',
#     'hold.mp3',
#     'find.mp3'
# ]

# # Helper function to handle transcription and send response back
# async def handle_full_sentence(full_sentence, websocket):
#     await websocket.send_text(full_sentence)

# @app.websocket("/ws/conversation")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     try:
#         while True:
#             selected_audio = random.choice(audio_files)
#             audio_segment = AudioSegment.from_file(selected_audio)

#             # Listen to user input and process
#             await get_transcript(handle_full_sentence, audio_segment)

#             if "goodbye" in transcription.lower():
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

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import os
import asyncio
import random
from pydub import AudioSegment
from io import BytesIO
from my_bot import ConversationManager, TextToSpeech, get_transcript
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

app = FastAPI()

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

# List of waiting audio prompts
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

    # Send initial waiting audio to the client
    selected_audio = random.choice(audio_files)
    audio_segment = AudioSegment.from_file(selected_audio, format="mp3")  # Ensure format is specified
    wav_buffer = BytesIO()
    audio_segment.export(wav_buffer, format="wav")  # Export to WAV format
    await websocket.send_bytes(wav_buffer.getvalue())  # Send audio bytes

    manager = ConversationManager()
    deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))
    dg_connection = await deepgram.listen.asynclive.v1()  # FIXED: Corrected Deepgram connection

    transcript_collector = get_transcript()

    async def on_message(result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if not result.speech_final:
            transcript_collector.add_part(sentence)
        else:
            transcript_collector.add_part(sentence)
            full_sentence = transcript_collector.get_full_transcript().strip()
            if full_sentence:
                print(f"Human: {full_sentence}")

                # Process with LLM
                llm_response = manager.llm.process(full_sentence)

                # Convert response to audio
                tts = TextToSpeech()
                audio_bytes = tts.speak(llm_response)

                # Send generated speech audio back to client
                await websocket.send_bytes(audio_bytes)

                # Reset transcript
                transcript_collector.reset()

    # Attach Deepgram event listener
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    # Set Deepgram options
    options = LiveOptions(
        model="nova-2-phonecall",
        punctuate=True,
        language="en-US",
        encoding="linear16",
        channels=1,
        sample_rate=16000,
        endpointing=300,
        smart_format=True,
    )

    await dg_connection.start(options)

    try:
        while True:
            # Receive raw audio bytes from client
            audio_chunk = await websocket.receive_bytes()
            await dg_connection.send(audio_chunk)  # FIXED: Added 'await'

    except WebSocketDisconnect:
        await dg_connection.finish()
        print("Client disconnected")

# Running the API using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
