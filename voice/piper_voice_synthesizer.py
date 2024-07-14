import threading
from piper.voice import PiperVoice
import pyaudio


class VoiceSynthesizer:

    def __init__(self, voice_model='voice/en_US-lessac-medium.onnx'):
        self._piper = PiperVoice.load(
            voice_model,
            config_path=f'{voice_model}.json',
            use_cuda=False
        )
        self._pyaudio = pyaudio.PyAudio()
        self._audio_stream = None
        self._make_stream_lock = threading.Lock()
        self._play_stream_lock = threading.Lock()

    def __del__(self):
        self._pyaudio.terminate()
    

    @property
    def is_making_stream(self):
        return self._make_stream_lock.is_locked()
    
    @property
    def is_playing_stream(self):
        return self._play_stream_lock.is_locked()
    


    def make_stream(self, text):
        with self._make_stream_lock:
            synthesize_args = {
                'length_scale': 1.5,
                'sentence_silence': 0.5,
            }

            text = ''.join([char for char in text if ord(char) < 128])  # Text filtering that cannot synthesize speech
            self._audio_stream = self._piper.synthesize_stream_raw(text, **synthesize_args)

    def play_stram(self):
        with self._play_stream_lock:
            stream = self._pyaudio.open(
                format=pyaudio.paInt16,  # S16_LE corresponds to paInt16 in pyaudio
                channels=1,              # Mono audio (single channel)
                rate=22050,              # Sample rate of 22050 Hz
                output=True
            )

            for audio_bytes in self._audio_stream:
                stream.write(audio_bytes)
            self._audio_stream = None

            stream.stop_stream()
            stream.close()

    def make_stream_async(self, text):
        threading.Thread(target=self.make_stream, args=(text,)).start()

    def play_stream_async(self):
        threading.Thread(target=self.play_stram).start()




if __name__ == '__main__':
    synthesizer = VoiceSynthesizer()
    synthesizer.synthesize('A rainbow is a meteorological phenomenon that is caused by reflection, \
        refraction and dispersion of light in water droplets resulting in a spectrum of light appearing in the sky.')