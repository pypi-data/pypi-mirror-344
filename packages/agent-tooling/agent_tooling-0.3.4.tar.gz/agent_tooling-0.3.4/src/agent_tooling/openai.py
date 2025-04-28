import json
from openai import OpenAI
from .tool import get_tool_schemas, get_tool_function
from typing import Any, Dict, List, Tuple, Generator

def get_tools(tags: list[str] = None) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """OpenAI tool schema wrapper"""
    functions = get_tool_schemas()

    tools = []
    available_functions = {}

    for function in functions:
        tools.append({
            "type": "function",
            "function": {
                "name": function["name"],
                "description": function["description"],
                "parameters": function["parameters"],
                "return_type": function["return_type"],
            },
        })
        
        func_name = function["name"]
        available_functions[func_name] = get_tool_function(func_name)

    return tools, available_functions

class OpenAITooling:
    def __init__(
            self, 
            api_key: str = None, 
            model: str = None,
            tool_choice: str = "auto"):
        self.api_key = api_key
        self.model = model
        self.tool_choice = tool_choice

    def call_tools(
            self,
            messages: list[dict[str, str]], 
            api_key: str = None, 
            model: str = None,
            tool_choice: str = "auto",
            tags: list[str] = None) -> list[dict[str,str]] | Generator[str, None, None]:
        """Handles OpenAI API tool calls."""

        if not api_key:
            api_key = self.api_key
        if not model:
            model = self.model

        """Interprets a user query and returns a standardized response dict."""

        client = OpenAI(api_key=api_key)

        tools, available_functions = get_tools(tags=tags)
        messages = messages

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        response = completion.choices[0].message
        tool_calls = response.tool_calls
        
        if tool_calls:
            for tool_call in tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                function_to_call = available_functions[name]

                # if there is an argument called messages, remove it from the args
                if "messages" in args:
                    del args["messages"]
                
                # Tool functions now return standardized responses
                result = function_to_call(**args, messages=messages)

                if isinstance(result, Generator):
                    for item in result:
                        yield item
                else:
                    messages.append({
                        "role": "function",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": result
                    })
                    return messages

        