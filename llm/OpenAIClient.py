import os
import threading
from openai import OpenAI

class OpenAIClient:

    def __init__(self, model='gpt-3.5-turbo-0125'):
        self.client = OpenAI()
        self.answer = None
        self.lock = threading.Lock()
        self.model = model

    def chat(self, text):
        with self.lock:
            self.answer = ''
            stream = self.client.chat.completions.create(
                model=self.model,
                stream=True,
                messages=[{
                    'role': 'user',
                    'content': text
                }]
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    self.answer += chunk.choices[0].delta.content

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
    client = OpenAIClient()
    client.chat_async('Why is the sky blue?')

    while True:
        if client.get_answer() is not None:
            print(client.get_answer())
            break