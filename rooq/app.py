from flask import Flask, request, jsonify, render_template
import os
import re
import webbrowser
from threading import Timer

app = Flask(__name__)

def create_structure(structure, base_path="."):
    lines = structure.split('\n')
    path_stack = []
    root_folder = None
    
    for line in lines:
        if not line.strip():
            continue
        
        # Count the depth based on the position of the last '├──' or '└──'
        depth = line.rfind('├──')
        if depth == -1:
            depth = line.rfind('└──')
        depth = depth // 4 if depth != -1 else 0
        
        # Remove all tree-like characters and leading/trailing whitespace
        name = re.sub(r'^[\s│├─└]+', '', line).strip()
        
        if root_folder is None:
            root_folder = name
            path_stack = [name]
            full_path = os.path.join(base_path, name)
            os.makedirs(full_path, exist_ok=True)
            continue
        
        # Adjust the path stack based on the depth
        while len(path_stack) > depth + 1:
            path_stack.pop()
        
        # Append the new item to the path stack
        path_stack = path_stack[:depth + 1] + [name]
        
        full_path = os.path.join(base_path, *path_stack)
        
        if name:
            if '.' in name:  # It's a file
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    pass  # Create an empty file
            else:  # It's a directory
                os.makedirs(full_path, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_files():
    structure = request.json['structure']
    try:
        create_structure(structure)
        return jsonify({"message": "Structure created successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

def run_app():
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    run_app()
