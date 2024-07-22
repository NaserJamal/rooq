import os
from pathlib import Path

def get_api_key():
    env_path = Path.home() / '.rooq_env'
    print(f"Checking for API key in: {env_path}")
    if env_path.exists():
        try:
            with open(env_path, 'r') as f:
                key = f.read().strip()
                if key.startswith('sk-'):
                    print("Valid API key found")
                    return key
                else:
                    print("API key found but it doesn't start with 'sk-'. It might be invalid.")
                    return None
        except Exception as e:
            print(f"Error reading API key: {e}")
    print("API key not found")
    return None

def save_api_key(api_key):
    env_path = Path.home() / '.rooq_env'
    try:
        with open(env_path, 'w') as f:
            f.write(api_key)
        print(f"API key saved to: {env_path}")
    except Exception as e:
        print(f"Error saving API key: {e}")

def ensure_api_key():
    api_key = get_api_key()
    if not api_key:
        print("No valid API key found. Please enter a new one.")
        api_key = input("Please enter your OpenAI API key: ").strip()
        if not api_key.startswith('sk-'):
            print("Warning: This doesn't look like a valid OpenAI API key. It should start with 'sk-'.")
        save_api_key(api_key)
    os.environ['OPENAI_API_KEY'] = api_key
    print(f"API key set in environment: {api_key[:5]}...")  # Print first 5 chars for verification