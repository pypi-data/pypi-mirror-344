# TransPhrase

TransPhrase is an AI-powered tool for translating web novels and other text content using various language models.

## Features

- Supports translation between multiple languages (English, Chinese, Japanese, Korean, Spanish, French, German, etc.)
- Interactive model selection with real-time filtering
- Automatic caching of translations to avoid redundant API calls
- Adaptive rate limiting to prevent API quota exhaustion
- Multi-threaded processing for faster translation
- Database tracking of translation jobs and progress
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
4. Select source and target languages
5. Choose a prompt template (translation or polishing)
6. Configure additional options

## Language Support

TransPhrase supports translation between the following languages:
- English
- Chinese
- Japanese
- Korean
- Spanish
- French
- German
- Russian
- Italian
- Portuguese
- Dutch
- Arabic
- Hindi

## Configuration

TransPhrase looks for an API key in the `MASTER_API_KEY` environment variable. You can set this in your environment or provide it when prompted.

## Advanced Features

### Rate Limiting

TransPhrase includes an adaptive rate limiter that:
- Dynamically adjusts to API feedback
- Handles 429 (Too Many Requests) errors gracefully
- Implements backoff strategies for reliable operation
- Adjusts concurrent workers based on API limits

### Translation Caching

All translations are cached locally to:
- Avoid redundant API calls for identical text
- Reduce costs and speed up batch processing
- Provide resilience during network interruptions

## Development

### Testing

Run tests with pytest:

```bash
pytest
```

### Publishing

The package is automatically published to PyPI when a new release is created on GitHub.

## Requirements

- Python 3.9+
- OpenAI API key or compatible API endpoint

## License

MIT
