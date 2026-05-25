from dotenv import load_dotenv
from anthropic import Anthropic
from DateTimeTool import get_current_datetime_schema, get_current_datetime
import DateTimeTool
from anthropic.types import ToolUseBlock, TextBlock

load_dotenv()

client = Anthropic()
haiku = "claude-haiku-4-5-20251001"
sonnet = "claude-sonnet-4-6"

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages, system_prompt=None, temperature=None, toolSchemas=None):
    params = {
        "model": haiku,
        "max_tokens": 200,
        "messages": messages,
    }
    if system_prompt:
        params["system"] = system_prompt
    if temperature is not None:
        params["temperature"] = temperature
    if toolSchemas:
        params["tools"] = toolSchemas
    return client.messages.create(**params)

def UseTool(ToolName, Input):
    if ToolName == "get_current_datetime":
        return get_current_datetime(**Input)
    if ToolName == "add_duration":
        return DateTimeTool.add_duration(**Input)


def conversation(messages, continueConversation,UserMessageRequired):

    while continueConversation:

        if UserMessageRequired:
            add_user_message(messages, input())
            print("System: UserMessage Added")

        response = chat(messages, toolSchemas=DateTimeTool.all_tools)

        for block in response.content:
            if isinstance(block, ToolUseBlock):
                UserMessageRequired = False
                print("System: Tool use request received for " + block.name)
                ToolCallResult = UseTool(block.name, block.input)
                messages.append({"role": "assistant", "content": response.content})
                messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": ToolCallResult
                    }]
                })
                print("System: Tool use response sent")
            elif isinstance(block, TextBlock):
                print("\n" + block.text + "\n")
                UserMessageRequired = True


continueConversation = True
UserMessageRequired = True
messages = []
result = conversation(messages, continueConversation, UserMessageRequired)

