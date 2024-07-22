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
        "Return only the fixed line of code without any explanations or code block markers. "
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Fix this code to pass the Flake8 test:\nErrors:\n{error_messages}\nCode:\n{code_line}"}
            ]
        )
        fixed_code = response.choices[0].message['content'].strip()
        
        # Remove code block markers if present
        fixed_code = re.sub(r'^```python\n|^```\n|```$', '', fixed_code, flags=re.MULTILINE).strip()
        
        # Preserve original indentation
        original_indent = len(code_line) - len(code_line.lstrip())
        fixed_code = ' ' * original_indent + fixed_code.lstrip()
        
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