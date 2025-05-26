Chatbot With Website

This script creates a simple chatbot that extracts text from a given website and allows users to ask questions about the content of that website. It uses OpenAI's API for answering questions based on the extracted content.

## Features

- Extracts text content from a given website.
- Preprocesses the extracted text for better analysis.
- Uses OpenAI's GPT model to answer user questions about the website content.

## Requirements

### Python Version

- Python 3.10 or later is required.

### Dependencies

The following Python packages are required to run the script:

- `requests`
- `beautifulsoup4`
- `re` (built-in)
- `getpass` (built-in)
- `autogen-agentchat`
- `autogen-ext[openai]`
- `openai`
- `PyQt5==5.15.7`
- `easyocr`
- `asyncio` (built-in)

You can install the required dependencies using the `requirements.txt` file provided in the `AutoGen Framework` directory:

```bash
pip install -r "AutoGen Framework/requirements.txt"