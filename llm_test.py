import sys


import llm
import voice


client = llm.OllamaClient()
voice = voice.VoiceSynthesizer()

answer = client.chat('Why is the the sky blue?')
print(answer)

voice.synthesis(answer)