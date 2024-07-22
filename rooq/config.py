import os
from pathlib import Path

def get_api_key():
    env_path = Path.home() / '.rooq_env'
    print(f"Checking for API key in: {env_path}")
    if env_path.exists():
        with open(env_path, 'r') as f:
            key = f.read().strip()
            print("API key found")
            return key
    print("API key not found")
    return None

def save_api_key(api_key):
    env_path = Path.home() / '.rooq_env'
    with open(env_path, 'w') as f:
        f.write(api_key)
    print(f"API key saved to: {env_path}")

def ensure_api_key():
    api_key = get_api_key()
    if not api_key:
        api_key = input("Please enter your OpenAI API key: ")
        save_api_key(api_key)
    os.environ['OPENAI_API_KEY'] = api_key
    print(f"API key set in environment: {api_key[:5]}...")  # Print first 5 chars for verification