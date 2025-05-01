<p align="center">
    <a href="https://pypi.org/project/shllm/">
        <img src="https://img.shields.io/pypi/v/shllm?color=3772A5" /></a>
</p>

# shllm
  
Generate shell commands using natural language.

## Installation

```bash
echo "export SHLLM_OPENAI_KEY={{OpenAI API Key}}" >> ~/.zshrc
pip install uv
uv pip install shllm
```

Alternatively:

```bash
echo "export SHLLM_OPENAI_KEY={{OpenAI API Key}}" >> ~/.zshrc
pipx install shllm
```

## Usage
```bash
shllm {{what you want to do}}
```
### Example
```bash
shllm show how many gigabytes of free space I have left on my hard drive
Command: df -h . | awk 'NR==2 {print $4}'
Would you like to run this command? [y]es/[n]o: y
Running: df -h . | awk 'NR==2 {print $4}'
425Gi
```

## Features

- **Direct command execution**: Run generated commands with simple yes/no confirmation
- **Smart command generation**: Uses advanced AI to translate natural language to shell commands
- **Non-interactive mode**: Automatically detects non-interactive environments and skips prompts