import pyaudio
import socket

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
        data, addr = sock.recvfrom(CHUNK * 2)  # Receive audio data
        stream.write(data)  # Play the received audio data
except KeyboardInterrupt:
    pass

# Close the stream and socket
stream.stop_stream()
stream.close()
audio.terminate()
sock.close()
