import pyaudio
import socket

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Network parameters
HOST = '192.168.1.33'  # Broadcast to all IPs
PORT = 5000

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, frames_per_buffer=CHUNK)

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Broadcasting...")

try:
    while True:
        data = stream.read(CHUNK)
        sock.sendto(data, (HOST, PORT))
except KeyboardInterrupt:
    pass

# Close the stream and socket
stream.stop_stream()
stream.close()
audio.terminate()
sock.close()
