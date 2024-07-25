import os
from pathlib import Path

def get_api_key():
    env_path = Path.home() / '.rooq_env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            return f.read().strip()
    return None

def save_api_key(api_key):
    env_path = Path.home() / '.rooq_env'
    with open(env_path, 'w') as f:
        f.write(api_key)
    print("API key saved successfully.")

def ensure_api_key():
    api_key = get_api_key()
    if not api_key:
        api_key = input("Please enter your OpenAI API key: ")
        save_api_key(api_key)
    os.environ['OPENAI_API_KEY'] = api_key

def update_api_key():
    new_key = input("Enter your new OpenAI API key: ")
    save_api_key(new_key)
    os.environ['OPENAI_API_KEY'] = new_key