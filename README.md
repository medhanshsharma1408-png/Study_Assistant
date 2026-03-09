# AI Study Assistant

A terminal-based AI assistant that helps users learn topics, generate quizzes, and get definitions by combining a **Large Language Model with external APIs**.

## Features

- Topic explanations using the **Wikipedia API**

- Quiz generation using the **Open Trivia DB API**

- Word definitions using the **Dictionary API**

- **Automatic prompt routing** to the appropriate tool

- **Retry logic** for API failures

- **Logging** of prompts, responses, and token usage

## Tech Stack

- Python

- Groq API (LLM)

- Requests

- Logging module

## Setup

Clone the repository

git clone [GitHub](https://github.com/yourusername/ai-study-assistant.git)
cd ai-study-assistant

Install dependencies

pip install groq requests

Set your API key

export GROQ_API_KEY=your_api_key

(Windows)

setx GROQ_API_KEY "your_api_key"

Run the assistant

python chatbot_logic.py

## Example Prompts

explain photosynthesis
define entropy
create a hard quiz on computer science

## Project Structure

- chatbot_logic.py   # routing logic
- LLM.py             # LLM + API integrations
- config.py          # model configuration
- ui.py              # CLI input

## Logging

Logs are stored in:

- assistant.log

They include:

- user prompts

- API calls

- model responses

- token usage

## License

MIT
