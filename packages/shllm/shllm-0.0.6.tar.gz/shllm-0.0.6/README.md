<p align="center">
    <a href="https://pypi.org/project/shllm/">
        <img src="https://img.shields.io/pypi/v/shllm?color=3772A5" /></a>
</p>

# shllm
  
Generate shell commands using natural langauge.

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
Command to be copied to clipboard: df -h . | awk 'NR==2 {print $4}'
What would you like to do? [c]opy to clipboard, [r]un the command, [q]uit: c
Command has been copied to the clipboard.
```

## Features

- **Cross-platform clipboard support**: Works in various environments including SSH sessions
- **Multiple clipboard backends**: Automatically tries different clipboard mechanisms based on your environment:
  - Desktop environments: pyperclip
  - macOS: pbcopy
  - Linux X11: xclip, xsel
  - Linux Wayland: wl-copy
  - Android (Termux): termux-clipboard-set
  - Windows: clip
- **Run directly**: Execute commands directly without copying
- **Non-interactive mode**: Automatically detects non-interactive environments (like CI pipelines) and skips prompts