# Rooq

Rooq is a wrapper on Flake8 that uses GPT-4o mini to automatically fix code to pass Flake8 tests.

## Installation

You can install Rooq using pip:

pip install rooq

## Usage

To use Rooq, simply run the following command in your terminal:

rooq [DIRECTORY]

If no directory is specified, Rooq will run on the current directory.

## How it works

1. Rooq runs a Flake8 lint scan on the specified directory.
2. For each Flake8 error, Rooq extracts the relevant code and sends it to the GPT-4 API along with the error message.
3. GPT-4 generates a fix for the code.
4. Rooq prompts you to apply the fix or skip it.
5. If you choose to apply the fix, Rooq automatically updates the file with the fixed code.

## Requirements

- Python 3.6+
- OpenAI API key

## License

This project is licensed under the MIT License.