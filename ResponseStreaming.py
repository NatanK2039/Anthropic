from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5-20251001"
system_prompt="Always answer in one sentance."
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message) 

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

messages = []

add_user_message(messages, "What is the date today?")



with client.messages.stream(
    model=model,
    max_tokens = 200,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="")
        pass

#stream.get_final_message() GETS THE FINAL MESSAGE AFTER COMBINING CHUNKS