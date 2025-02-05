import asyncio
import websockets
import pyaudio
import io
from pydub import AudioSegment
from pydub.playback import play

# Audio Configuration
CHUNK_SIZE = 4096  # Increased chunk size
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

def record_audio_chunk(stream, chunk_size=CHUNK_SIZE):
    """Records a chunk of audio from the microphone."""
    return stream.read(chunk_size, exception_on_overflow=False)

async def send_audio_to_server(uri):
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server.")

            # Set up PyAudio for recording
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK_SIZE)

            print("Speaking...")

            # Start receiving audio in parallel
            receive_task = asyncio.create_task(receive_audio(websocket))

            try:
                while True:
                    # Record audio in chunks and send to server
                    audio_chunk = record_audio_chunk(stream)
                    print(f"Sending audio chunk: {len(audio_chunk)} bytes")
                    await websocket.send(audio_chunk)
                    await asyncio.sleep(0.1)  # Prevent overwhelming the server

            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed.")
            except KeyboardInterrupt:
                print("Recording interrupted by user.")
            finally:
                receive_task.cancel()
                try:
                    await receive_task
                except asyncio.CancelledError:
                    pass  # Task was cancelled, ignore
                # Cleanup
                stream.stop_stream()
                stream.close()
                p.terminate()

    except websockets.exceptions.WebSocketException as e:
        print(f"WebSocket Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

async def receive_audio(websocket):
    """Receives and plays audio from the WebSocket server."""
    try:
        while True:
            # Receive audio response from server
            audio_data = await websocket.recv()
            if isinstance(audio_data, bytes):
                print(f"Received {len(audio_data)} bytes of audio.")
                try:
                    audio = AudioSegment.from_raw(io.BytesIO(audio_data), sample_width=2, frame_rate=RATE, channels=CHANNELS)
                    print(f"Playing received audio: {len(audio_data)} bytes")
                    play(audio)
                except Exception as e:
                    print(f"Error processing audio data: {e}")
            else:
                print(f"Received non-audio data: {audio_data}")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed.")
    except Exception as e:
        print(f"Error receiving audio: {e}")

# Run the WebSocket client
uri = "ws://192.168.1.5:8000/ws/conversation"  # Adjust to your server IP
try:
    asyncio.run(send_audio_to_server(uri))
except KeyboardInterrupt:
    print("Client interrupted. Exiting...")
