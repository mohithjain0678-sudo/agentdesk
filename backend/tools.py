import httpx
import os

async def web_search(query: str) -> str:
    """Search the web using DuckDuckGo instant answer API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.duckduckgo.com/",
                params={
                    "q": query,
                    "format": "json",
                    "no_html": "1",
                    "skip_disambig": "1"
                },
                timeout=10.0
            )
            data = response.json()
            
            result = ""
            if data.get("AbstractText"):
                result += f"Summary: {data['AbstractText']}\n"
            if data.get("RelatedTopics"):
                topics = data["RelatedTopics"][:3]
                for topic in topics:
                    if isinstance(topic, dict) and topic.get("Text"):
                        result += f"- {topic['Text']}\n"
            
            return result if result else f"No instant results found for: {query}. Try rephrasing."
    except Exception as e:
        return f"Search error: {str(e)}"


async def read_file(filepath: str) -> str:
    """Read a file from the filesystem"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return f"File contents of {filepath}:\n{content}"
    except FileNotFoundError:
        return f"File not found: {filepath}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


async def write_file(filepath: str, content: str) -> str:
    """Write content to a file"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


async def list_files(directory: str = ".") -> str:
    """List files in a directory"""
    try:
        files = os.listdir(directory)
        return f"Files in {directory}:\n" + "\n".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}"


# Tool registry — agent uses this to know what tools exist
TOOLS = {
    "web_search": {
        "function": web_search,
        "description": "Search the web for information",
        "parameters": {"query": "string — the search query"}
    },
    "read_file": {
        "function": read_file,
        "description": "Read contents of a file",
        "parameters": {"filepath": "string — path to the file"}
    },
    "write_file": {
        "function": write_file,
        "description": "Write content to a file",
        "parameters": {"filepath": "string — path to file", "content": "string — content to write"}
    },
    "list_files": {
        "function": list_files,
        "description": "List files in a directory",
        "parameters": {"directory": "string — directory path, default is current directory"}
    }
}