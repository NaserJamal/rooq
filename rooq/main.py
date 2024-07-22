import os
from .flake8_runner import run_flake8
from .gpt_fixer import fix_code
from .config import ensure_api_key

def run_rooq(directory):
    ensure_api_key()
    
    if input("Run rooq? (y/n): ").lower() != 'y':
        print("Rooq execution cancelled.")
        return

    flake8_output = run_flake8(directory)
    if not flake8_output:
        print("No Flake8 issues found.")
        return

    for file_path, errors in flake8_output.items():
        print(f"Fixing issues in {file_path}")
        print("Flake8 errors:")
        for error in errors:
            print(error)
        
        with open(file_path, 'r') as file:
            original_code = file.read()
        
        error_messages = '\n'.join(errors)
        fixed_code = fix_code(original_code, error_messages)

        if fixed_code:
            print("\nDo you want to see a diff of the changes? (y/n): ")
            if input().lower() == 'y':
                show_diff(original_code, fixed_code)
            
            if input("Apply this fix? (y/n): ").lower() == 'y':
                with open(file_path, 'w') as file:
                    file.write(fixed_code)
                print("Fix applied.")
            else:
                print("Fix not applied.")
        else:
            print(f"Couldn't generate a fix for {file_path}")

def show_diff(original, fixed):
    import difflib
    d = difflib.Differ()
    diff = list(d.compare(original.splitlines(), fixed.splitlines()))
    for line in diff:
        if line.startswith('+'):
            print('\033[92m' + line + '\033[0m')  # Green for additions
        elif line.startswith('-'):
            print('\033[91m' + line + '\033[0m')  # Red for deletions
        elif line.startswith('?'):
            print('\033[94m' + line + '\033[0m')  # Blue for changes
        else:
            print(line)

def parse_flake8_output(output):
    parts = output.split(':')
    file_path = parts[0]
    line_number = int(parts[1])
    error_message = ':'.join(parts[3:]).strip()
    return file_path, line_number, error_message

def get_code_from_file(file_path, line_number):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines[line_number - 1].strip()

def apply_fix(file_path, line_number, fixed_code):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    lines[line_number - 1] = fixed_code + '\n'
    
    with open(file_path, 'w') as file:
        file.writelines(lines)