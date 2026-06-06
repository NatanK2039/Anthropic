from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import ToolUseBlock, TextBlock
from LoggerRebuild1 import log
from UserInterfaceRebuild import append_message
import ToolRegistryRebuild

load_dotenv()

client = Anthropic()
sonnet = "claude-sonnet-4-6"
messages = []

def chat(messages, system_prompt="You have access to a tool called list_tools and get_tool_schema. Before answering any question that may require real-time data or calculations, use list_tools to discover available tools, then get_tool_schema to learn their inputs.", temperature=None, toolSchemas=None):
    params = {
        "model": sonnet,
        "max_tokens": 1024,
        "messages": messages,
    }
    if system_prompt:
        params["system"] = system_prompt
    if temperature is not None:
        params["temperature"] = temperature
    if toolSchemas:
        params["tools"] = toolSchemas
    return client.messages.create(**params)


def conversation(user_input, output):
    messages.append({"role": "user", "content": user_input})
    log("User message added")

    needs_tool_call = True
    while needs_tool_call:
        response = chat(messages, toolSchemas=ToolRegistryRebuild.discovery_tools)
        log("\n" + str(response) + "\n")

        tool_results = []

        for block in response.content:
            if isinstance(block, ToolUseBlock):
                log("Tool use request received for " + block.name)
                ToolCallResult = ToolRegistryRebuild.dispatch(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": ToolCallResult
                })
            elif isinstance(block, TextBlock):
                append_message(output, "Claude", block.text)

        if tool_results:
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
            log("Tool use response sent")
        else:
            needs_tool_call = False