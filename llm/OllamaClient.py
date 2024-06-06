import asyncio
import ollama

class OllamaClient:

    def __init__(self, model='tinyllama', system_prompt=''):
        self.messages = []
        if system_prompt is not '':
            self.messages.append({'role': 'system', 'content': system_prompt})

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