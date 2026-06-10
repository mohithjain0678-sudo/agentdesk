import json
import re
from groq import AsyncGroq
from tools import TOOLS
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are AgentDesk, a powerful AI assistant that can use tools to complete tasks.

You have access to these tools:
- web_search(query): Search the web for information
- read_file(filepath): Read contents of a file
- write_file(filepath, content): Write content to a file
- list_files(directory): List files in a directory

When you need to use a tool, respond EXACTLY in this format:
TOOL_CALL: tool_name
PARAMS: {"param1": "value1"}

IMPORTANT RULES:
- Use each tool MAXIMUM once per task
- After getting a tool result, always give a final answer to the user
- Never call the same tool twice in a row
- If a tool returns no results, answer from your own knowledge
- Always end with a direct helpful response to the user"""

async def run_agent(user_message: str, conversation_history: list) -> dict:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})
    
    actions_taken = []
    max_iterations = 5
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        
        assistant_message = response.choices[0].message.content
        
        if "TOOL_CALL:" in assistant_message:
            tool_result = await handle_tool_call(assistant_message, actions_taken)
            messages.append({"role": "assistant", "content": assistant_message})
            messages.append({"role": "user", "content": f"Tool Result: {tool_result}"})
        else:
            return {
                "response": assistant_message,
                "actions": actions_taken
            }
    
    return {
        "response": "Max actions reached.",
        "actions": actions_taken
    }


async def handle_tool_call(message: str, actions_taken: list) -> str:
    try:
        tool_match = re.search(r"TOOL_CALL:\s*(\w+)", message)
        params_match = re.search(r"PARAMS:\s*(\{.*?\})", message, re.DOTALL)
        
        if not tool_match:
            return "Error: Could not parse tool name"
        
        tool_name = tool_match.group(1).strip()
        params = {}
        
        if params_match:
            params = json.loads(params_match.group(1))
        
        if tool_name not in TOOLS:
            return f"Error: Unknown tool '{tool_name}'"
        
        tool_func = TOOLS[tool_name]["function"]
        result = await tool_func(**params)
        
        actions_taken.append({
            "tool": tool_name,
            "params": params,
            "result": result[:200] + "..." if len(result) > 200 else result
        })
        
        return result
        
    except json.JSONDecodeError:
        return "Error: Could not parse parameters"
    except Exception as e:
        return f"Tool error: {str(e)}"