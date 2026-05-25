
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5-20251001"
system_prompt="Always answer in one sentence."
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

def eval(Dataset):
    pass

messages = []

userMessage = input()

add_user_message(messages, userMessage)

assistantResponse = chat(messages, system_prompt, 0)

add_assistant_message(messages, assistantResponse)


print("begin eval")
evalResults = chat(messages, "Evaluate quality of message: Give 0-10 rating with very short justification. Max 150 tokens total.", 0)
print(evalResults)

print("done")

#stream.get_final_message() GETS THE FINAL MESSAGE AFTER COMBINING CHUNKS