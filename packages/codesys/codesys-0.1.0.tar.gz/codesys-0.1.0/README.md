# LMSYS SDK

A Python SDK for interacting with the Claude CLI tool.

## Installation

```bash
pip install lmsys
```

## Requirements

- Python 3.8+
- Claude CLI tool must be installed and available in your PATH

## Quick Start

```python
from lmsys import Agent

# Initialize with a working directory
agent = Agent(working_dir="/path/to/your/project")

# Run Claude with a prompt
result = agent.run("Your prompt here")
print(result)

# Auto-streaming output (prints automatically)
lines = agent.run("Generate a story", stream=True)

# Manual streaming (if you need more control)
process = agent.run("Another prompt", stream=True, auto_print=False)
for line in process.stdout:
    print(line, end="")
```

## Features

- Simple interface to the Claude CLI tool
- Support for all Claude CLI options
- Automatic or manual streaming output
- Customizable tool access

## API Reference

### Agent Class

```python
Agent(working_dir=None, allowed_tools=None)
```

**Parameters:**
- `working_dir` (str, optional): The working directory for Claude to use. Defaults to current directory.
- `allowed_tools` (list, optional): List of tools to allow Claude to use. Defaults to ["Edit", "Bash", "Write"].

### Methods

#### run

```python
run(prompt, stream=False, output_format=None, additional_args=None, auto_print=True)
```

Run Claude with the specified prompt.

**Parameters:**
- `prompt` (str): The prompt to send to Claude.
- `stream` (bool): If True, handles streaming output. If False, returns the complete output.
- `output_format` (str, optional): Optional output format (e.g., "stream-json").
- `additional_args` (dict, optional): Additional arguments to pass to the Claude CLI.
- `auto_print` (bool): If True and stream=True, automatically prints output. If False, you need to handle streaming manually.

**Returns:**
- If `stream=False`: Returns the complete output as a string.
- If `stream=True` and `auto_print=False`: Returns a subprocess.Popen object for manual streaming.
- If `stream=True` and `auto_print=True`: Automatically prints output and returns collected lines as a list.

#### run_with_tools

```python
run_with_tools(prompt, tools, stream=False, auto_print=True)
```

Run Claude with specific allowed tools.

**Parameters:**
- `prompt` (str): The prompt to send to Claude.
- `tools` (list): List of tools to allow Claude to use.
- `stream` (bool): If True, handles streaming output.
- `auto_print` (bool): If True and stream=True, automatically prints output.

**Returns:**
- If `stream=False`: Returns the complete output as a string.
- If `stream=True` and `auto_print=False`: Returns a subprocess.Popen object.
- If `stream=True` and `auto_print=True`: Automatically prints output and returns collected lines.

## Example: Automatic Streaming

```python
from lmsys import Agent

agent = Agent()
# This will automatically print the output line by line
lines = agent.run("Generate a short story", stream=True)
```

## Example: Manual Streaming with JSON parsing

```python
from lmsys import Agent
import json

agent = Agent()
process = agent.run("Generate a short story", stream=True, output_format="stream-json", auto_print=False)

for line in process.stdout:
    if line.strip():
        try:
            data = json.loads(line)
            print(data.get("content", ""))
        except json.JSONDecodeError:
            print(f"Error parsing JSON: {line}")
```

## License

MIT