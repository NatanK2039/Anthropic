from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import ToolUseBlock, TextBlock
from Logger import logThis
import ToolRegistry
load_dotenv()

client = Anthropic()
sonnet = "claude-sonnet-4-6"

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def chat(messages, system_prompt="You have access to a tool called list_tools and get_tool_schema. Before answering any question that may require real-time data or calculations, use list_tools to discover available tools, then get_tool_schema to learn their inputs.", temperature=None, toolSchemas=None):
    params = {
        "model": sonnet,
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


def conversation(messages, continueConversation, UserMessageRequired):
    logThis("\n\n\n\n\n------------- New Conversation -------------")

    while continueConversation:

        if UserMessageRequired:
            add_user_message(messages, input())
            logThis("UserMessage Added")

        response = chat(messages, toolSchemas=ToolRegistry.discovery_tools)

        logThis("\n" + str(response) + "\n")

        tool_results = []

        for block in response.content:
            if isinstance(block, ToolUseBlock):
                UserMessageRequired = False
                logThis("Tool use request received for " + block.name)
                ToolCallResult = ToolRegistry.dispatch(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": ToolCallResult
                })
            elif isinstance(block, TextBlock):
                print(block.text)
                UserMessageRequired = True

        if tool_results:
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
            logThis("Tool use response sent")


continueConversation = True
UserMessageRequired = True
messages = []
result = conversation(messages, continueConversation, UserMessageRequired)