import os
from collections import defaultdict
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
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        errors_by_line = defaultdict(list)
        for error in errors:
            line_num, col, error_msg = parse_flake8_error(error)
            errors_by_line[line_num].append(f"{col}: {error_msg}")
        
        fixes = []
        for line_num, line_errors in errors_by_line.items():
            original_line = lines[line_num - 1]
            error_messages = '\n'.join(line_errors)
            fixed_line = fix_code(original_line, error_messages)

            if fixed_line and fixed_line != original_line:
                fixes.append((line_num, original_line, fixed_line))
            elif fixed_line == original_line:
                print(f"No changes needed for line {line_num}")
            else:
                print(f"Couldn't generate a fix for line {line_num}")
        
        if fixes:
            print("\nProposed fixes:")
            for line_num, original, fixed in fixes:
                print(f"\nLine {line_num}:")
                print("Original:", original.rstrip())
                print("Fixed:   ", fixed.rstrip())
            
            if input("\nApply all these fixes? (y/n): ").lower() == 'y':
                for line_num, _, fixed_line in fixes:
                    lines[line_num - 1] = fixed_line
                
                # Write the fixed content back to the file
                with open(file_path, 'w') as file:
                    file.writelines(lines)
                print("All fixes applied.")
            else:
                print("No fixes applied.")
        else:
            print("No fixes were generated.")

def parse_flake8_error(error):
    parts = error.split(':')
    line_num = int(parts[0])
    col = parts[1]
    error_msg = ':'.join(parts[2:]).strip()
    return line_num, col, error_msg