import asyncio
import time
from AppKit import NSSpeechSynthesizer


class VoiceSynthesizer:

    def __init__(self, voice_model='com.apple.voice.compact.en-US.Samantha'):
        self.speech = NSSpeechSynthesizer.alloc().initWithVoice_(voice_model)

    def synthesis(self, text):
        self.speech.startSpeakingString_(text)
        while self.speech.isSpeaking():
            pass

    async def synthesis_async(self, text):
        self.speech.startSpeakingString_(text)
        while self.speech.isSpeaking():
            asyncio.sleep(1)


if __name__ == '__main__':
    synthesizer = VoiceSynthesizer()
    synthesizer.synthesis('A rainbow is a meteorological phenomenon that is caused by reflection, \
        refraction and dispersion of light in water droplets resulting in a spectrum of light appearing in the sky.')