import openai
import os
import re
import traceback
from .config import ensure_api_key

def fix_code(code, error_messages):
    ensure_api_key()
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: No API key found in environment variables.")
        return None
    
    openai.api_key = api_key
    print(f"OpenAI API key set: {api_key[:5]}...")  # Print first 5 chars for verification

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
        "6. W291: Trailing whitespace\n"
        "7. W293: Blank line contains whitespace\n"
        "Ensure that all these issues are addressed in your fix."
    )

    try:
        print("Sending request to OpenAI API...")
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # or "gpt-4" if available
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Fix this code to pass the Flake8 test:\n\nErrors:\n{error_messages}\n\nCode:\n{code}"}
            ]
        )
        print("Response received from OpenAI API.")
        fixed_code = response.choices[0].message['content'].strip()
        
        # Remove Python code block markers if present
        fixed_code = re.sub(r'^```python\n|^```\n|```$', '', fixed_code, flags=re.MULTILINE)
        
        # Apply post-processing fixes
        # fixed_code = fix_long_lines(fixed_code)
        # fixed_code = remove_trailing_whitespace(fixed_code)
        # fixed_code = fix_blank_lines_with_whitespace(fixed_code)
        
        # Ensure there's a newline at the end of the file
        if not fixed_code.endswith('\n'):
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
        print("Traceback:")
        traceback.print_exc()
        return None

# def fix_long_lines(code):
#     lines = code.split('\n')
#     fixed_lines = []
#     for line in lines:
#         if len(line) > 79:
#             # Check if it's a comment
#             if line.strip().startswith('#'):
#                 fixed_lines.append(line[:79])
#                 fixed_lines.append('#' + line[79:])
#             # Check if it's a string
#             elif ('"' in line or "'" in line) and line.count('"') % 2 == 0 or line.count("'") % 2 == 0:
#                 fixed_lines.append(line[:line.index('"') + 1] + '\\')
#                 fixed_lines.append(line[line.index('"') + 1:])
#             # Check if it's a function call or definition
#             elif '(' in line and ')' in line:
#                 open_paren = line.index('(')
#                 fixed_lines.append(line[:open_paren+1])
#                 args = line[open_paren+1:-1].split(',')
#                 for arg in args[:-1]:
#                     fixed_lines.append(f"    {arg.strip()},")
#                 fixed_lines.append(f"    {args[-1].strip()})")
#             # If we can't find a good breaking point, just split at 79
#             else:
#                 fixed_lines.append(line[:79] + '\\')
#                 fixed_lines.append('    ' + line[79:])
#         else:
#             fixed_lines.append(line)
#     return '\n'.join(fixed_lines)

# def remove_trailing_whitespace(code):
#     return '\n'.join(line.rstrip() for line in code.split('\n'))

# def fix_blank_lines_with_whitespace(code):
#     lines = code.split('\n')
#     return '\n'.join('' if line.strip() == '' else line for line in lines)