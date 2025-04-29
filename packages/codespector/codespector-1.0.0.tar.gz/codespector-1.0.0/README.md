# CodeSpector

CodeSpector is a Python package designed to review code changes for quality and security issues using AI chat agents. It supports different chat agents like Codestral and ChatGPT.

## Features

- Automated code review using AI chat agents.
- Supports multiple chat agents and models.
- Generates detailed review reports in markdown format.
- Configurable via environment variables and command-line options.

## Installation

To install the package, use the following command:

```sh
pip install codespector
```

```sh
uv add codespector
```

## Usage

### Command-Line Interface

You can use the `codespector` command to start a code review. Below are the available options:

```sh
Usage: codespector [OPTIONS]

Options:
  --chat-token TEXT          Chat agent token  [env var: CODESPECTOR_CHAT_TOKEN]
  --chat-model TEXT          Choose the chat model to use  [env var: CODESPECTOR_CHAT_MODEL]
  --chat-agent TEXT          Choose the chat agent to use (codestral, chatgpt, deepseek)
                            or set your own  [env var: CODESPECTOR_CHAT_AGENT]
  -b, --compare-branch TEXT  Select the branch to compare the current one with
  --output-dir TEXT         Select the output directory  [default: codespector]
                            [env var: CODESPECTOR_OUTPUT_DIR]
  --system-content TEXT     Content which used in system field for agent
                            [env var: CODESPECTOR_SYSTEM_CONTENT]
  --prompt-content TEXT     Prompt content which included to review prompt
                            [env var: CODESPECTOR_PROMPT_CONTENT]
  --result-file TEXT        Set file for saving the result
                            [env var: CODESPECTOR_RESULT_FILE]
  --exclude-file-ext LIST   Exclude file extensions from the review
                            [env var: CODESPECTOR_EXCLUDE_FILE_EXT]
  --version                 Show the version and exit.
  --help                    Show this message and exit.
```

### Example

To run a code review, use the following command:

```sh
codespector --chat-token YOUR_CHAT_TOKEN --chat-agent codestral --compare-branch develop --result-file result.md --system-content "system content" --prompt-content "prompt content"
```

## Configuration

You can also configure CodeSpector using environment variables. Create a `.env` file in the root directory of your project with the following content:

```
CODESPECTOR_CHAT_TOKEN=your_token
CODESPECTOR_OUTPUT_DIR=codespector
CODESPECTOR_SYSTEM_CONTENT="Ты код ревьювер. Отвечай на русском"
CODESPECTOR_PROMPT_CONTENT="Оцени код на безопасноть, соблюдение лучших техник"
CODESPECTOR_RESULT_FILE="result.md"
CODESPECTOR_CHAT_AGENT=codestral
CODESPECTOR_CHAT_MODEL=your_model
CODESPECTOR_EXCLUDE_FILE_EXT=.pyc,.pyo
```

## Makefile Commands

- `lint`: Run linting and formatting checks.
- `format`: Format the code.
- `fix`: Fix linting issues and format the code.
- `test`: Run the tests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.