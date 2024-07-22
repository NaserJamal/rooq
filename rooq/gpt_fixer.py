import openai
import os
import re
from .config import ensure_api_key

def fix_code(code_line, error_messages):
    ensure_api_key()
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: No API key found in environment variables.")
        return None
    
    openai.api_key = api_key

    system_prompt = (
        "You are an AI assistant that fixes Python code to pass Flake8 tests. "
        "Your task is to fix lines that are too long (over 79 characters) by breaking them into multiple lines. "
        "Return only the fixed code without any explanations or code block markers."
    )

    user_prompt = (
        f"Fix this code to pass the Flake8 test:\n"
        f"Error: {error_messages}\n"
        f"Code: {code_line}\n"
        f"Remember to break the line to be 79 characters or less."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        fixed_code = response.choices[0].message['content'].strip()
        
        print("API Response:", fixed_code)  # Debug print
        
        # Remove code block markers if present
        fixed_code = re.sub(r'^```python\n|^```\n|```$', '', fixed_code, flags=re.MULTILINE).strip()
        
        # Preserve original indentation for each line
        original_indent = len(code_line) - len(code_line.lstrip())
        fixed_lines = fixed_code.split('\n')
        fixed_code = '\n'.join(' ' * original_indent + line.lstrip() for line in fixed_lines)
        
        # Ensure the fixed code ends with a newline if the original did
        if code_line.endswith('\n') and not fixed_code.endswith('\n'):
            fixed_code += '\n'
        
        return fixed_code
    except openai.error.AuthenticationError:
        print("Authentication error: Your API key may be invalid or expired.")
        return None
    except openai.error.RateLimitError:
        print("Rate limit exceeded: You've hit the API rate limit. Please try again later.")
        return None
    except Exception as e:
        print(f"Error occurred while calling the OpenAI API: {e}")
        return None