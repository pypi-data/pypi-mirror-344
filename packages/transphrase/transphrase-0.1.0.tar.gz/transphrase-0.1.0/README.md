# TransPhrase

TransPhrase is an AI-powered tool for translating web novels and other text content using various language models.

## Features

- Supports multiple AI models for translation
- Interactive model selection with real-time filtering
- Automatic caching of translations to avoid redundant API calls
- Rate limiting to prevent API quota exhaustion
- Multi-threaded processing for faster translation
- Database tracking of translation jobs
- Plugin system for custom prompt templates

## Installation

### Using pip

```bash
pip install transphrase
```

### From source

```bash
git clone https://github.com/shinyPy/TransPhrase.git
cd TransPhrase
pip install -e .
```

## Usage

Once installed, you can run TransPhrase from the command line:

```bash
transphrase
```

Follow the interactive prompts to configure your translation job:

1. Enter the source directory containing text files to translate
2. Select an output directory
3. Choose a language model
4. Select a prompt template
5. Configure additional options

## Configuration

TransPhrase looks for an API key in the `MASTER_API_KEY` environment variable. You can set this in your environment or provide it when prompted.

## Requirements

- Python 3.7+
- OpenAI API key or compatible API endpoint

## License

MIT
