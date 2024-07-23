import subprocess

def run_flake8(directory):
    result = subprocess.run(['flake8', directory], capture_output=True, text=True)
    errors = {}
    if result.stdout:
        for line in result.stdout.strip().split('\n'):
            parts = line.split(':', 3)
            if len(parts) >= 4:
                file_path = parts[0]
                if file_path not in errors:
                    errors[file_path] = []
                errors[file_path].append(':'.join(parts[1:]))
    return errors