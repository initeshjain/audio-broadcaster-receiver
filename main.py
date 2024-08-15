import pyaudio
import socket

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050  # Lower sample rate for testing
CHUNK = 2048  # Increased buffer size

# Network parameters
HOST = '192.168.241.255'  # Broadcast address
PORT = 5000

# Initialize PyAudio
audio = pyaudio.PyAudio()

# List available input devices
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    device_info = audio.get_device_info_by_host_api_device_index(0, i)
    if device_info.get('maxInputChannels') > 0:
        print(f"Input Device ID {i} - {device_info.get('name')}")

# Open stream (using device index 2 as per your code)
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, input_device_index=2, frames_per_buffer=CHUNK)

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcasting

print("Broadcasting...")

try:
    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            sock.sendto(data, (HOST, PORT))
        except IOError as e:
            print(f"Buffer overflow: {e}")
            continue  # Skip the corrupted chunk
except KeyboardInterrupt:
    pass

# Close the stream and socket
stream.stop_stream()
stream.close()
audio.terminate()
sock.close()
