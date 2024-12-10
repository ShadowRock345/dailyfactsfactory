import openai
from logger import Config

global model,temperature,max_tokens

config = Config('CHATGPT')
model = str(config.getvalue('model'))
temperature = float(config.getvalue('temperature'))
max_tokens = int(config.getvalue('max_tokens'))

class ChatGPT:
    def __init__(self):
        pass
    
    def generate(self,prompt):
        global model,temperature,max_tokens
        response = openai.Completion.create(model=model,prompt=prompt,temperature=temperature,max_tokens=max_tokens)
        return response
#model