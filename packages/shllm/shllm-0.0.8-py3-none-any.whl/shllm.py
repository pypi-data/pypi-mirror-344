#!/usr/bin/env python3

import sys
import os
import subprocess
from openai import OpenAI

def is_interactive():
    """Check if the script is running in an interactive environment"""
    return os.isatty(sys.stdin.fileno()) if hasattr(sys.stdin, 'fileno') else False

def main():
    if os.getenv('SHLLM_OPENAI_KEY') is None:
        print("Error: SHLLM_OPENAI_KEY environment variable is not set.")
        sys.exit(1)

    prompt = ' '.join(sys.argv[1:])
    client = OpenAI(api_key=os.getenv('SHLLM_OPENAI_KEY'))
    role = 'You are shell helper. Given a question, answer with just a shell command, nothing else. Do not wrap it in markdown.'

    try:
        model = os.getenv('OPENAI_MODEL', 'gpt-4o')

        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": role},
                      {"role": "user", "content": prompt}],
            model=model
        )

        result_prompt = chat_completion.choices[0].message.content
        
        # For backwards compatibility with previous output format
        print("Command: " + result_prompt)
        
        # Skip interactive prompts in non-interactive environments
        if not is_interactive():
            return
            
        while True:
            try:
                action = input(f"Would you like to run this command? [y]es/[n]o: ").lower()
                
                if action in ['y', 'yes']:
                    print(f"Running: {result_prompt}")
                    try:
                        subprocess.run(result_prompt, shell=True)
                    except Exception as e:
                        print(f"Error running command: {str(e)}")
                    break
                elif action in ['n', 'no']:
                    break
                else:
                    print("Invalid option. Please enter 'y' or 'n'.")
            except EOFError:
                # Handle non-interactive environments gracefully
                break
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("An error occurred:", str(e))


if __name__ == "__main__":
    main()