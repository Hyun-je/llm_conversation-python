import asyncio
import ollama

class OllamaClient:

    def __init__(self, model='tinyllama'):
        pass

    def chat(self, text):
        answer = ''
        stream = ollama.chat(
            model='tinyllama',
            stream=True,
            messages=[{
                'role': 'user',
                'content': text
            }]
        )

        for chunk in stream:
            # print(chunk['message']['content'], end='', flush=True)
            answer += chunk['message']['content']

        # print('')

        return answer

if __name__ == '__main__':
    client = OllamaClient()
    answer = client.chat('Why is the sky blue?')
    print(answer)