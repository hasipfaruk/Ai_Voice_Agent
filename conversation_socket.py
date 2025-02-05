from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydub import AudioSegment
from io import BytesIO
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from groq import Groq  # Import Groq SDK/Client
from my_bot import ConversationManager, TextToSpeech, get_transcript
import os
import random
import asyncio

app = FastAPI()

audio_files = ['wait.wav', 'patiant.wav', 'checking.wav', 'getting.wav', 'hold.wav', 'find.wav']

@app.websocket("/ws/conversation")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        # Load API Keys
        deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not deepgram_api_key or not groq_api_key:
            print("Error: Missing API keys!")
            await websocket.close()
            return

        # Send initial waiting audio
        selected_audio = random.choice(audio_files)
        audio_segment = AudioSegment.from_file(selected_audio, format="wav")
        wav_buffer = BytesIO()
        audio_segment.export(wav_buffer, format="wav")
        await websocket.send_bytes(wav_buffer.getvalue())

        # Initialize Deepgram client
        deepgram = DeepgramClient(api_key=deepgram_api_key)

        # Create live transcription connection
        print("Initializing Deepgram live transcription...")
        dg_connection = await deepgram.listen.live.v("1")
        transcript_collector = await get_transcript(callback=None, audio_segment=None)

        # Initialize Groq client
        groq_client = Groq(api_key=groq_api_key)

        async def on_message(result, **kwargs):
            """Handles incoming transcriptions from Deepgram"""
            sentence = result.channel.alternatives[0].transcript
            if not result.speech_final:
                transcript_collector.add_part(sentence)
            else:
                transcript_collector.add_part(sentence)
                full_sentence = transcript_collector.get_full_transcript().strip()
                if full_sentence:
                    print(f"Human: {full_sentence}")

                    # Process with Groq LLM
                    groq_response = await groq_generate_response(groq_client, full_sentence)

                    # Convert response to audio
                    tts = TextToSpeech()
                    audio_bytes = await tts.speak(groq_response)

                    # Send generated speech audio back to client
                    print(f"Sending audio: {len(audio_bytes)} bytes")
                    await websocket.send_bytes(audio_bytes)

                    # Reset transcript
                    transcript_collector.reset()

        # Attach event listener for transcription
        async def handle_transcription(result, **kwargs):
            await on_message(result)

        dg_connection.on(LiveTranscriptionEvents.Transcript, handle_transcription)

        # Configure Deepgram options
        options = LiveOptions(
            model="nova-2-phonecall",
            language="en-US",
            smart_format=True,
            encoding="linear16",
            sample_rate=16000,
            channels=1
        )

        # Start the Deepgram connection
        print("Starting Deepgram connection...")
        await dg_connection.start(options)

        while True:
            # Receive raw audio bytes from client
            audio_chunk = await websocket.receive_bytes()
            print(f"Received {len(audio_chunk)} bytes from client.")
            try:
                await dg_connection.send(audio_chunk)  # Send audio to Deepgram
            except Exception as e:
                print(f"Error sending audio to Deepgram: {e}")
                await websocket.send_text("Error processing audio.")
                break

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Unexpected error: {e}")
        await websocket.close()
    finally:
        try:
            await dg_connection.finish()
            print("Deepgram WebSocket connection closed.")
        except Exception as e:
            print(f"Error closing Deepgram WebSocket: {e}")

async def groq_generate_response(groq_client, prompt):
    """Handles asynchronous request to Groq's LLM"""
    try:
        response = await groq_client.call_model(prompt)
        return response["text"]
    except Exception as e:
        print(f"Error in Groq LLM: {e}")
        return "I encountered an error."

# Running the API using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
