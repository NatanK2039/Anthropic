from datetime import datetime, timedelta
from anthropic.types import ToolParam

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
            "days": {
                "type": "integer",
                "description": "Number of days to add (can be negative)."
            },
            "hours": {
                "type": "integer",
                "description": "Number of hours to add (can be negative)."
            },
            "minutes": {
                "type": "integer",
                "description": "Number of minutes to add (can be negative)."
            },
            "seconds": {
                "type": "integer",
                "description": "Number of seconds to add (can be negative)."
            },
            "date_format": {
                "type": "string",
                "description": "A strftime format string (e.g. '%Y-%m-%d %H:%M:%S')."
            }
        },
        "required": ["base_datetime"]
    }
}

all_tools = [get_current_datetime_schema, add_duration_schema]


def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)


def add_duration(base_datetime, days=0, hours=0, minutes=0, seconds=0, date_format="%Y-%m-%d %H:%M:%S"):
    base = datetime.strptime(base_datetime, "%Y-%m-%d %H:%M:%S")
    result = base + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return result.strftime(date_format)