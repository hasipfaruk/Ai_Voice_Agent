# # import asyncio
# # import websockets

# # async def websocket_client():
# #     uri = "ws://192.168.1.5:8000/ws/conversation"  # URL of the WebSocket server
# #     while True:  # Run indefinitely to reconnect if disconnected
# #         try:
# #             # async with websockets.connect(uri) as websocket:
# #             async with websockets.connect(uri, open_timeout=60) as websocket:
# #                 print("Connected to WebSocket server.")
                
# #                 # Send the initial message
# #                 await websocket.send("Hello, server!")
# #                 print("Message sent to the server: Hello, server!")
                
# #                 # Continuously receive messages from the server
# #                 while True:
# #                     try:
# #                         response = await websocket.recv()  # Wait for a message from the server
# #                         print(f"Received from server: {response}")
                        
# #                         # Optionally, send another message back to the server
# #                         user_input = input("You: ")
# #                         await websocket.send(user_input)
# #                         print(f"Message sent to server: {user_input}")
# #                     except websockets.exceptions.ConnectionClosed:
# #                         print("Connection closed by the server.")
# #                         break
# #         except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.WebSocketException) as e:
# #             print(f"Error: {e}")
# #             print("Reconnecting in 3 seconds...")
# #             await asyncio.sleep(3)  # Wait before reconnecting

# # # Run the WebSocket client
# # asyncio.run(websocket_client())




# # this is new code for testing :
# # import asyncio
# # import websockets
# # import pyaudio
# # import wave
# # import io
# # from pydub import AudioSegment
# # from pydub.playback import play

# # # Audio recording settings
# # FORMAT = pyaudio.paInt16
# # CHANNELS = 1
# # RATE = 16000  # Sample rate
# # CHUNK = 1024
# # RECORD_SECONDS = 3  # Duration per recording segment

# # async def record_and_send_audio(websocket):
# #     """ Records audio from the microphone and sends it to the server. """
# #     audio = pyaudio.PyAudio()
# #     stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
# #     print("🎤 Recording...")
# #     frames = []

# #     for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
# #         data = stream.read(CHUNK)
# #         frames.append(data)

# #     print("📤 Sending audio to server...")
# #     stream.stop_stream()
# #     stream.close()
# #     audio.terminate()

# #     # Convert frames to WAV format
# #     wav_buffer = io.BytesIO()
# #     wf = wave.open(wav_buffer, 'wb')
# #     wf.setnchannels(CHANNELS)
# #     wf.setsampwidth(audio.get_sample_size(FORMAT))
# #     wf.setframerate(RATE)
# #     wf.writeframes(b''.join(frames))
# #     wf.close()

# #     await websocket.send(wav_buffer.getvalue())  # Send audio data

# # async def websocket_client():
# #     uri = "ws://192.168.1.5:8000/ws/conversation"  # Update with your server IP

# #     while True:
# #         try:
# #             async with websockets.connect(uri) as websocket:
# #                 print("✅ Connected to WebSocket server.")

# #                 while True:
# #                     await record_and_send_audio(websocket)  # 🎤 Send voice input

# #                     # ✅ Receive AI response (audio)
# #                     response_audio = await websocket.recv()
                    
# #                     # ✅ Play AI response
# #                     print("🔊 Playing AI response...")
# #                     audio_segment = AudioSegment.from_file(io.BytesIO(response_audio), format="wav")
# #                     play(audio_segment)

# #         except websockets.exceptions.ConnectionClosed:
# #             print("⚠️ Connection closed. Reconnecting in 3 seconds...")
# #             await asyncio.sleep(3)

# # # Run the WebSocket client
# # asyncio.run(websocket_client())


# # import asyncio
# # import websockets
# # import pyaudio
# # import wave
# # import os
# # import atexit

# # # Set up audio recording
# # def record_audio():
# #     CHUNK = 1024
# #     FORMAT = pyaudio.paInt16
# #     CHANNELS = 1
# #     RATE = 16000
# #     RECORD_SECONDS = 5  # You can adjust the recording time
# #     WAVE_OUTPUT_FILENAME = "output.wav"

# #     p = pyaudio.PyAudio()

# #     stream = p.open(format=FORMAT,
# #                     channels=CHANNELS,
# #                     rate=RATE,
# #                     input=True,
# #                     frames_per_buffer=CHUNK)
# #     print("Recording...")
# #     frames = []

# #     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
# #         data = stream.read(CHUNK)
# #         frames.append(data)

# #     print("Recording finished.")
# #     stream.stop_stream()
# #     stream.close()
# #     p.terminate()

# #     with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
# #         wf.setnchannels(CHANNELS)
# #         wf.setsampwidth(p.get_sample_size(FORMAT))
# #         wf.setframerate(RATE)
# #         wf.writeframes(b''.join(frames))

# #     return WAVE_OUTPUT_FILENAME

# # # Send audio to the WebSocket server
# # async def send_audio_to_server(uri):
# #     async with websockets.connect(uri) as websocket:
# #         print("Connected to WebSocket server.")

# #         # Record audio and send to the server
# #         audio_file = record_audio()
# #         with open(audio_file, 'rb') as f:
# #             audio_data = f.read()

# #         await websocket.send(audio_data)
# #         print("Audio sent to server.")

# #         # Receive audio from server and play it
# #         response = await websocket.recv()  # Receive audio data from the server
# #         with open("received_audio.wav", 'wb') as f:
# #             f.write(response)  # Save received audio
# #         print("Received audio from server, playing it...")

# #         # Play the received audio
# #         os.system("ffplay -nodisp -autoexit received_audio.wav")

# # # Function to handle program exit and close WebSocket connection
# # def on_exit():
# #     print("Program terminating. Closing WebSocket connection.")

# # # Register the on_exit function to be called when the program exits
# # atexit.register(on_exit)

# # # Run the WebSocket client
# # uri = "ws://192.168.1.5/ws/conversation"  # Your server URI
# # try:
# #     asyncio.run(send_audio_to_server(uri))
# # except KeyboardInterrupt:
# #     print("Client program interrupted. Exiting...")
# #     # The connection is automatically closed on program termination due to the context manager in the `websockets.connect()`.







# # import asyncio
# # import websockets
# # import pyaudio
# # import wave
# # import os
# # import atexit
# # import time

# # # Set up audio recording
# # def record_audio_chunk(stream, chunk_size=1024):
# #     """Record a chunk of audio."""
# #     return stream.read(chunk_size)

# # # Send audio to the WebSocket server in chunks
# # async def send_audio_to_server(uri):
# #     async with websockets.connect(uri) as websocket:
# #         print("Connected to WebSocket server.")

# #         # Set up audio recording
# #         p = pyaudio.PyAudio()
# #         stream = p.open(format=pyaudio.paInt16,
# #                         channels=1,
# #                         rate=16000,
# #                         input=True,
# #                         frames_per_buffer=1024)
# #         print("Recording...")

# #         try:
# #             while True:
# #                 # Record audio in chunks and send them over the WebSocket connection
# #                 audio_chunk = record_audio_chunk(stream)
# #                 await websocket.send(audio_chunk)

# #                 # Wait for a response (audio from the server)
# #                 response = await websocket.recv()  # Receive audio data from the server

# #                 # Save received audio as a .wav file
# #                 with open("received_audio.wav", 'wb') as f:
# #                     f.write(response)
# #                 print("Received audio from server, playing it...")

# #                 # Play the received audio
# #                 os.system("ffplay -nodisp -autoexit received_audio.wav")

# #         except KeyboardInterrupt:
# #             print("Recording interrupted by user.")
# #         finally:
# #             # Clean up
# #             stream.stop_stream()
# #             stream.close()
# #             p.terminate()

# # # Function to handle program exit and close WebSocket connection
# # def on_exit():
# #     print("Program terminating. Closing WebSocket connection.")

# # # Register the on_exit function to be called when the program exits
# # atexit.register(on_exit)

# # # Run the WebSocket client
# # uri = "ws://192.168.1.5:8000/ws/conversation"  # Your server URI (replace with actual IP)
# # try:
# #     asyncio.run(send_audio_to_server(uri))
# # except KeyboardInterrupt:
# #     print("Client program interrupted. Exiting...")














# # import asyncio
# # import websockets
# # import pyaudio
# # import wave
# # import os
# # import atexit
# # import time
# # from pydub import AudioSegment
# # from pydub.playback import play

# # # Set up audio recording
# # def record_audio_chunk(stream, chunk_size=1024):
# #     """Record a chunk of audio."""
# #     return stream.read(chunk_size)

# # # Send audio to the WebSocket server in chunks
# # async def send_audio_to_server(uri):
# #     async with websockets.connect(uri) as websocket:
# #         print("Connected to WebSocket server.")

# #         # Set up audio recording
# #         p = pyaudio.PyAudio()
# #         stream = p.open(format=pyaudio.paInt16,
# #                         channels=1,
# #                         rate=16000,
# #                         input=True,
# #                         frames_per_buffer=1024)
# #         print("Recording...")

# #         try:
# #             while True:
# #                 # Record audio in chunks and send them over the WebSocket connection
# #                 audio_chunk = record_audio_chunk(stream)
# #                 await websocket.send(audio_chunk)

# #                 # Wait for a response (audio from the server)
# #                 response = await websocket.recv()  # Receive audio data from the server

# #                 # Save received audio as a .wav file
# #                 with open("received_audio.wav", 'wb') as f:
# #                     f.write(response)
# #                 print("Received audio from server, playing it...")

# #                 # Play the received audio
# #                 os.system("ffplay -nodisp -autoexit received_audio.wav")

# #         except KeyboardInterrupt:
# #             print("Recording interrupted by user.")
# #         finally:
# #             # Clean up
# #             stream.stop_stream()
# #             stream.close()
# #             p.terminate()

# # # Function to handle program exit and close WebSocket connection
# # def on_exit():
# #     print("Program terminating. Closing WebSocket connection.")

# # # Register the on_exit function to be called when the program exits
# # atexit.register(on_exit)

# # # Run the WebSocket client
# # uri = "ws://192.168.1.5:8000/ws/conversation"  # Your server URI (replace with actual IP)
# # try:
# #     asyncio.run(send_audio_to_server(uri))
# # except KeyboardInterrupt:
# #     print("Client program interrupted. Exiting...")




# # import asyncio
# # import websockets
# # import pyaudio
# # import wave
# # import os
# # import atexit
# # import time
# # from pydub import AudioSegment
# # from pydub.playback import play

# # # Set up audio recording
# # def record_audio_chunk(stream, chunk_size=1024):
# #     """Record a chunk of audio."""
# #     return stream.read(chunk_size)

# # # Send audio to the WebSocket server in chunks
# # async def send_audio_to_server(uri):
# #     async with websockets.connect(uri) as websocket:
# #         print("Connected to WebSocket server.")

# #         # Set up audio recording
# #         p = pyaudio.PyAudio()
# #         stream = p.open(format=pyaudio.paInt16,
# #                         channels=1,
# #                         rate=16000,
# #                         input=True,
# #                         frames_per_buffer=1024)
# #         print("Recording...")

# #         try:
# #             while True:
# #                 # Record audio in chunks and send them over the WebSocket connection
# #                 audio_chunk = record_audio_chunk(stream)
# #                 await websocket.send(audio_chunk)

# #                 # Wait for a response (audio from the server)
# #                 response = await websocket.recv()  # Receive audio data from the server

# #                 # Save received audio as a .wav file
# #                 with open("received_audio.wav", 'wb') as f:
# #                     f.write(response)
# #                 print("Received audio from server, playing it...")

# #                 # Play the received audio
# #                 os.system("ffplay -nodisp -autoexit received_audio.wav")

# #         except KeyboardInterrupt:
# #             print("Recording interrupted by user.")
# #         finally:
# #             # Clean up
# #             stream.stop_stream()
# #             stream.close()
# #             p.terminate()

# # # Function to handle program exit and close WebSocket connection
# # def on_exit():
# #     print("Program terminating. Closing WebSocket connection.")

# # # Register the on_exit function to be called when the program exits
# # atexit.register(on_exit)

# # # Run the WebSocket client
# # uri = "ws://192.168.1.5:8000/ws/conversation"  # Your server URI (replace with actual IP)
# # try:
# #     asyncio.run(send_audio_to_server(uri))
# # except KeyboardInterrupt:
# #     print("Client program interrupted. Exiting...")

# import asyncio
# import websockets
# import pyaudio
# import io
# from pydub import AudioSegment
# from pydub.playback import play

# # Set up audio recording
# def record_audio_chunk(stream, chunk_size=1024):
#     """Record a chunk of audio."""
#     return stream.read(chunk_size)

# # Send audio to the WebSocket server in chunks
# async def send_audio_to_server(uri):
#     async with websockets.connect(uri) as websocket:
#         print("Connected to WebSocket server.")
#         p = pyaudio.PyAudio()
#         stream = p.open(format=pyaudio.paInt16,
#                         channels=1,
#                         rate=16000,
#                         input=True,
#                         frames_per_buffer=1024)
#         print("Recording...")

#         try:
#             while True:
#                 # Record a chunk of audio from the microphone
#                 audio_chunk = record_audio_chunk(stream)

#                 # Send the audio chunk to the WebSocket server
#                 await websocket.send(audio_chunk)

#                 # Wait for the bot's audio response
#                 bot_audio = await websocket.recv()

#                 # Play the received bot's audio response
#                 audio_segment = AudioSegment.from_file(io.BytesIO(bot_audio), format="wav")
#                 play(audio_segment)

#         except KeyboardInterrupt:
#             print("Recording interrupted by user.")
#         finally:
#             stream.stop_stream()
#             stream.close()
#             p.terminate()

# # Run the WebSocket client
# uri = "ws://192.168.1.5:8000/ws/conversation"  # Replace with actual server URI
# try:
#     asyncio.run(send_audio_to_server(uri))
# except KeyboardInterrupt:
#     print("Client program interrupted. Exiting...")



# import asyncio
# import websockets
# import pyaudio
# import os
# import atexit
# from pydub import AudioSegment
# from pydub.playback import play
# import io

# # Set up audio recording
# def record_audio_chunk(stream, chunk_size=1024):
#     """Record a chunk of audio."""
#     return stream.read(chunk_size)

# # Send audio to the WebSocket server in chunks
# async def send_audio_to_server(uri):
#     async with websockets.connect(uri) as websocket:
#         print("Connected to WebSocket server.")

#         # Set up audio recording
#         p = pyaudio.PyAudio()
#         stream = p.open(format=pyaudio.paInt16,
#                         channels=1,
#                         rate=16000,
#                         input=True,
#                         frames_per_buffer=1024)
#         print("Recording...")

#         # Start receiving task
#         receive_task = asyncio.create_task(receive_audio(websocket))

#         try:
#             while True:
#                 # Record audio in chunks and send them over the WebSocket connection
#                 audio_chunk = record_audio_chunk(stream)
#                 await websocket.send(audio_chunk)

#         except KeyboardInterrupt:
#             print("Recording interrupted by user.")
#         finally:
#             receive_task.cancel()
#             await receive_task
#             # Clean up
#             stream.stop_stream()
#             stream.close()
#             p.terminate()

# async def receive_audio(websocket):
#     try:
#         while True:
#             audio_data = await websocket.recv()
#             if isinstance(audio_data, bytes):
#                 # Play the audio
#                 audio = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
#                 play(audio)
#     except websockets.exceptions.ConnectionClosedOK:
#         print("Connection closed normally.")
#     except websockets.exceptions.ConnectionClosedError:
#         print("Connection closed with error.")

# # Function to handle program exit and close WebSocket connection
# def on_exit():
#     print("Program terminating. Closing WebSocket connection.")

# # Register the on_exit function to be called when the program exits
# atexit.register(on_exit)

# # Run the WebSocket client
# uri = "ws://192.168.1.5:8000/ws/conversation"  # Your server URI (replace with actual IP)
# try:
#     asyncio.run(send_audio_to_server(uri))
# except KeyboardInterrupt:
#     print("Client program interrupted. Exiting...")




import asyncio
import websockets
import pyaudio
import os
import atexit
from pydub import AudioSegment
from pydub.playback import play
import io

# Set up audio recording
def record_audio_chunk(stream, chunk_size=1024):
    """Record a chunk of audio."""
    return stream.read(chunk_size, exception_on_overflow=False)  # Fix for buffer overflow issues

# Send audio to the WebSocket server in chunks
async def send_audio_to_server(uri):
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server.")

            # Set up audio recording
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=16000,
                            input=True,
                            frames_per_buffer=1024)
            print("Recording...")

            # Start receiving task
            receive_task = asyncio.create_task(receive_audio(websocket))

            try:
                while True:
                    # Record audio in chunks and send them over the WebSocket connection
                    audio_chunk = record_audio_chunk(stream)
                    await websocket.send(audio_chunk)  # Ensure sending is awaited

            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed.")
            except KeyboardInterrupt:
                print("Recording interrupted by user.")
            finally:
                receive_task.cancel()
                try:
                    await receive_task
                except asyncio.CancelledError:
                    pass  # Task was cancelled, safe to ignore
                # Clean up
                stream.stop_stream()
                stream.close()
                p.terminate()

    except websockets.exceptions.WebSocketException as e:
        print(f"WebSocket Error: {e}")

async def receive_audio(websocket):
    """Receive and play audio from the WebSocket server."""
    try:
        while True:
            audio_data = await websocket.recv()
            if isinstance(audio_data, bytes):
                # Play the received audio
                audio = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
                play(audio)
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed normally.")
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed with error.")
    except Exception as e:
        print(f"Error receiving audio: {e}")

# Function to handle program exit and close WebSocket connection
def on_exit():
    print("Program terminating. Closing WebSocket connection.")

# Register the on_exit function to be called when the program exits
atexit.register(on_exit)

# Run the WebSocket client
uri = "ws://192.168.1.5:8000/ws/conversation"  # Your server URI (replace with actual IP)
try:
    asyncio.run(send_audio_to_server(uri))
except KeyboardInterrupt:
    print("Client program interrupted. Exiting...")
