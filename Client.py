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

def chat(messages, system_prompt, temperature):
    params = {
        "model": model,
        "max_tokens": 200,
        "messages": messages,
    }
    if system_prompt:
        params["system"] = system_prompt
    if temperature is not None:
        params["temperature"] = temperature

    message = client.messages.create (**params)
    return message.content[0].text

messages = []

add_user_message(messages, "Hello")

answer = chat(messages, None, None )

print(answer)

add_assistant_message(messages, answer)

while(True):
    add_user_message(messages, input("\nEnter your response\n"))
    answer = chat(messages, system_prompt, 1.0)
    print(answer + "\n")
    add_assistant_message(messages, answer)
    print(messages)

