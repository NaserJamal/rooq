import openai
import os
import re
from .config import ensure_api_key

def fix_code(code, error_messages):
    ensure_api_key()
    
    openai.api_key = os.environ['OPENAI_API_KEY']

    system_prompt = (
        "You are an AI assistant that fixes Python code to pass Flake8 tests. "
        "Return the entire fixed code without any explanations or code block markers. "
        "Preserve the original structure and comments of the code. "
        "Pay special attention to the following Flake8 rules:\n"
        "1. E501: Line too long (79 characters)\n"
        "   - Break long lines into multiple lines\n"
        "   - Use line continuation characters (\\) when necessary\n"
        "   - For long strings, use parentheses to break them across multiple lines\n"
        "2. E302: Expected 2 blank lines, found 1\n"
        "3. E301: Expected 1 blank line, found 0\n"
        "4. F811: Redefinition of unused name\n"
        "5. W292: No newline at end of file\n"
        "Ensure that all these issues are addressed in your fix."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # or "gpt-4" if available
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Fix this code to pass the Flake8 test:\n\nErrors:\n{error_messages}\n\nCode:\n{code}"}
            ]
        )
        fixed_code = response.choices[0].message['content'].strip()
        
        # Remove Python code block markers if present
        fixed_code = re.sub(r'^```python\n|^```\n|```$', '', fixed_code, flags=re.MULTILINE)
        
        # Post-processing to ensure long lines are fixed
        fixed_code = fix_long_lines(fixed_code)
        
        # Ensure there's a newline at the end of the file
        if not fixed_code.endswith('\n'):
            fixed_code += '\n'
        
        return fixed_code
    except Exception as e:
        print(f"Error occurred while calling the OpenAI API: {e}")
        return None

def fix_long_lines(code):
    lines = code.split('\n')
    fixed_lines = []
    for line in lines:
        if len(line) > 79:
            # Try to break the line at a sensible point
            if '=' in line:
                parts = line.split('=')
                fixed_lines.append(f"{parts[0].strip()} =")
                fixed_lines.append(f"    {parts[1].strip()}")
            elif '(' in line and ')' in line:
                # For function calls or definitions
                open_paren = line.index('(')
                fixed_lines.append(line[:open_paren+1])
                args = line[open_paren+1:-1].split(',')
                for arg in args[:-1]:
                    fixed_lines.append(f"    {arg.strip()},")
                fixed_lines.append(f"    {args[-1].strip()})")
            else:
                # If we can't find a good breaking point, just split at 79
                fixed_lines.append(line[:79])
                fixed_lines.append(line[79:])
        else:
            fixed_lines.append(line)
    return '\n'.join(fixed_lines)