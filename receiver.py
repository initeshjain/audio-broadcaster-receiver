import pyaudio
import socket
import struct

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Network parameters
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 5000

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open a stream for output
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print("Receiving audio...")

try:
    while True:
        # Receive audio data from sender
        data, addr = sock.recvfrom(CHUNK * 2)  # Receiving audio in chunks (2 bytes per sample for paInt16)
        
        # Optional: Validate data length
        if len(data) != CHUNK * 2:
            print("Received incomplete chunk")
            continue
        
        # Play the received audio data
        stream.write(data)
except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the stream and socket
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()
