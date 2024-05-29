import platform

if 'macOS' in platform.platform():
    from .mac_voice_synthesizer import VoiceSynthesizer
else:
    from .piper_voice_synthesizer import VoiceSynthesizer