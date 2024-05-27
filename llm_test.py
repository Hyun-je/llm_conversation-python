import sys
import ollama
from piper.voice import PiperVoice
import pyaudio




response = ollama.chat(model='tinyllama', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])

synthesize_args = {
    "length_scale": 1.5,
    "sentence_silence": 0.5,
}
voice = PiperVoice.load("en_US-lessac-medium.onnx", config_path="en_US-lessac-medium.onnx.json", use_cuda=False)
audio_stream = voice.synthesize_stream_raw(response['message']['content'], **synthesize_args)


# Initialize PyAudio
p = pyaudio.PyAudio()

# Define the audio stream properties to match aplay command
stream = p.open(format=pyaudio.paInt16,  # S16_LE corresponds to paInt16 in pyaudio
                channels=1,              # Mono audio (single channel)
                rate=22050,              # Sample rate of 22050 Hz
                output=True)

# Write and play the audio stream
for audio_bytes in audio_stream:
    stream.write(audio_bytes)

# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate PyAudio
p.terminate()