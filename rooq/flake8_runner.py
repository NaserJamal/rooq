import subprocess
from collections import defaultdict

def run_flake8(directory):
    result = subprocess.run(['flake8', directory], capture_output=True, text=True)
    errors = defaultdict(list)
    if result.stdout:
        for line in result.stdout.strip().split('\n'):
            parts = line.split(':')
            file_path = parts[0]
            error = ':'.join(parts[1:])
            errors[file_path].append(error)
    return dict(errors)