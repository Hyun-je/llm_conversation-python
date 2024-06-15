import asyncio
import threading
import ollama

class OllamaClient:
    def __init__(self, model='tinyllama', system_prompt=''):
        self.messages = []
        self.answer = None
        self.lock = threading.Lock()
        if system_prompt != '':
            self.messages.append({'role': 'system', 'content': system_prompt})

    def chat(self, text):
        with self.lock:
            self.answer = ''
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
                self.answer += chunk['message']['content']

        return self.answer
    
    def chat_async(self, text):
        threading.Thread(target=self.chat, args=(text,)).start()

    def is_running(self):
        return self.lock.locked()

    def get_answer(self):
        if self.lock.locked():
            return None
        else:
            return self.answer


if __name__ == '__main__':
    client = OllamaClient()

    client.chat_async('Why is the sky blue?')

    while True:
        if client.get_answer() is not None:
            print(client.get_answer())
            break
