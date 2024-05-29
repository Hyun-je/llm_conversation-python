from piper.voice import PiperVoice
import pyaudio


class VoiceSynthesizer:

    def __init__(self, voice_model='voice/en_US-lessac-medium.onnx'):
        self.piper = PiperVoice.load(
            voice_model,
            config_path=f'{voice_model}.json',
            use_cuda=False
        )
        self.pyaudio = pyaudio.PyAudio()

    def __del__(self):
        self.pyaudio.terminate()

    def synthesis(self, text):
        audio_stream = self.make_stream(text)
        self.play_stream(audio_stream)

    async def synthesis_async(self, text):
        self.synthesis(text)

    def make_stream(self, text):
        synthesize_args = {
            'length_scale': 1.5,
            'sentence_silence': 0.5,
        }
        audio_stream = self.piper.synthesize_stream_raw(text, **synthesize_args)

        return audio_stream

    def play_stream(self, audio_stream):
        stream = self.pyaudio.open(
            format=pyaudio.paInt16,  # S16_LE corresponds to paInt16 in pyaudio
            channels=1,              # Mono audio (single channel)
            rate=22050,              # Sample rate of 22050 Hz
            output=True
        )

        for audio_bytes in audio_stream:
            stream.write(audio_bytes)

        stream.stop_stream()
        stream.close()


if __name__ == '__main__':
    synthesizer = VoiceSynthesizer()
    synthesizer.synthesis('A rainbow is a meteorological phenomenon that is caused by reflection, \
        refraction and dispersion of light in water droplets resulting in a spectrum of light appearing in the sky.')