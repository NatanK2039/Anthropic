import json
from datetime import datetime, timedelta
from anthropic.types import ToolParam

# ── Schemas ──────────────────────────────────────────────────────────────────

get_current_datetime_schema: ToolParam = {
    "name": "get_current_datetime",
    "description": "Returns the current date and time formatted as a string.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "A strftime format string (e.g. '%Y-%m-%d %H:%M:%S'). Must not be empty."
            }
        },
        "required": []
    }
}

add_duration_schema: ToolParam = {
    "name": "add_duration",
    "description": "Adds a duration to a given base datetime and returns the result as a formatted string. You must provide the base datetime — use get_current_datetime first if needed.",
    "input_schema": {
        "type": "object",
        "properties": {
            "base_datetime": {
                "type": "string",
                "description": "The starting datetime string in '%Y-%m-%d %H:%M:%S' format."
            },
            "days": {"type": "integer", "description": "Number of days to add (can be negative)."},
            "hours": {"type": "integer", "description": "Number of hours to add (can be negative)."},
            "minutes": {"type": "integer", "description": "Number of minutes to add (can be negative)."},
            "seconds": {"type": "integer", "description": "Number of seconds to add (can be negative)."},
            "date_format": {"type": "string", "description": "A strftime format string (e.g. '%Y-%m-%d %H:%M:%S')."}
        },
        "required": ["base_datetime"]
    }
}

read_file_schema: ToolParam = {
    "name": "read_file",
    "description": "Reads the contents of a file and returns it as a string.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "The path to the file to read."}
        },
        "required": ["path"]
    }
}

write_file_schema: ToolParam = {
    "name": "write_file",
    "description": "Writes text content to a file, overwriting it if it exists.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "The path to the file to write."},
            "content": {"type": "string", "description": "The text content to write to the file."}
        },
        "required": ["path", "content"]
    }
}

list_tools_schema: ToolParam = {
    "name": "list_tools",
    "description": "Returns the names of all available tools.",
    "input_schema": {"type": "object", "properties": {}, "required": []}
}

get_tool_schema_schema: ToolParam = {
    "name": "get_tool_schema",
    "description": "Returns the full schema of a tool by name so you can understand its inputs before calling it.",
    "input_schema": {
        "type": "object",
        "properties": {
            "tool_name": {"type": "string", "description": "The name of the tool to retrieve the schema for."}
        },
        "required": ["tool_name"]
    }
}

# ── Tool lists ────────────────────────────────────────────────────────────────

all_tools = [
    get_current_datetime_schema,
    add_duration_schema,
    read_file_schema,
    write_file_schema,
    list_tools_schema,
    get_tool_schema_schema,
]

discovery_tools = [list_tools_schema, get_tool_schema_schema]

# ── Functions ─────────────────────────────────────────────────────────────────

def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)

def add_duration(base_datetime, days=0, hours=0, minutes=0, seconds=0, date_format="%Y-%m-%d %H:%M:%S"):
    base = datetime.strptime(base_datetime, "%Y-%m-%d %H:%M:%S")
    result = base + timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    return result.strftime(date_format)

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Written to {path}"

def list_tools():
    return ", ".join([t["name"] for t in all_tools])

def get_tool_schema(tool_name):
    schema_map = {t["name"]: t for t in all_tools}
    if tool_name not in schema_map:
        return f"Unknown tool: {tool_name}"
    return json.dumps(schema_map[tool_name], indent=2)

# ── Dispatch ──────────────────────────────────────────────────────────────────

def dispatch(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    if tool_name == "add_duration":
        return add_duration(**tool_input)
    if tool_name == "read_file":
        return read_file(**tool_input)
    if tool_name == "write_file":
        return write_file(**tool_input)
    if tool_name == "list_tools":
        return list_tools()
    if tool_name == "get_tool_schema":
        return get_tool_schema(**tool_input)
    return f"Unknown tool: {tool_name}"