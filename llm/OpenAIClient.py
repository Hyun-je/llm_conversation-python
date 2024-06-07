import os
from openai import OpenAI

class OpenAIClient:

    def __init__(self, model='gpt-3.5-turbo-0125'):
        self.client = OpenAI()
        self.model = model

    def chat(self, text):
        answer = ''

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
                answer += chunk.choices[0].delta.content

        return answer

if __name__ == '__main__':
    client = OpenAIClient()
    answer = client.chat('Why is the sky blue?')
    print(answer)