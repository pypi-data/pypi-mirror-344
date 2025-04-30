# TransPhrase

TransPhrase is an AI-powered tool for translating web novels and other text content using various language models.

## Features

- Supports translation between multiple languages (English, Chinese, Japanese, Korean, Spanish, French, German, etc.)
- Automatic language detection for source files
- Interactive model selection with real-time filtering
- Automatic caching of translations to avoid redundant API calls
- Adaptive rate limiting to prevent API quota exhaustion
- Multi-threaded processing for faster translation
- Database tracking of translation jobs and progress
- Plugin system for custom prompt templates
- Semantic text chunking for improved translation quality
- Dependency injection for better testability and maintainability
- Support for both translation and text polishing modes

## Operation Modes

TransPhrase supports two operation modes:

### Translation Mode

Converts text between different languages while maintaining tone, style, and meaning.

- Perfect for web novels, technical documents, or any text content
- Preserves character names, terms, and stylistic elements
- Optimized for context-aware translation across multiple files

### Polish Mode

Improves existing translations for better readability and fluency.

- Enhances grammar, flow, and natural phrasing
- Maintains character authenticity and consistent terminology
- Adds emotional depth while preserving the original plot
- Ideal for refining machine-translated content
- Works in any supported language, not just English

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

1. Select operation mode (translate or polish)
2. Choose a language model
3. Select source and target languages (or use auto-detection)
4. Enter the source directory containing text files to process
5. Select an output directory
6. Configure advanced options (caching, threading, etc.)
7. Start the translation process

### Command-line Arguments

TransPhrase supports the following command-line arguments:

```bash
# Run without saving configuration
transphrase --no-save-config

# Run with a fresh configuration (ignoring existing saved config)
transphrase --overwrite-config

# Disable automatic language detection:
transphrase --no-auto-detect
```

## Language Support

TransPhrase supports translation between languages depending on the capabilities of the selected language model (LLM). Commonly supported languages include:

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
- Vietnamese
- Thai
- Indonesian

Refer to the documentation of your chosen LLM for the full list of supported languages.

## Configuration

TransPhrase supports several configuration methods:

### Environment Variables

- `MASTER_API_KEY`: Your API key
- `API_BASE_URL`: Base URL for API calls (defaults to https://api.electronhub.top)

### Configuration File

TransPhrase can be configured using a JSON file located at `~/.transphrase/config.json`.
This allows you to save your settings and reuse them without going through the interactive prompts each time.

Example config.json:
```json
{
  "api_key": "your-api-key",
  "base_url": "https://api.electronhub.top",
  "model": "deepseek-llm-67b-chat",
  "source_language": "Japanese",
  "target_language": "English",
  "skip_existing": true,
  "workers": 8,
  "use_cache": true,
  "cache_ttl": 604800,
  "db_path": "~/.transphrase/novels.db",
  "plugins": {
    "prompt_template": "LightNovelTemplate",
    "processors": ["NameConsistencyProcessor", "DialogFormatter"]
  },
  "series_id": "my-light-novel-series",
  "auto_add_characters": false,
  "name_frequency_threshold": 15,
  "auto_detect_language": true
}
```

## Advanced Features

### Automatic Language Detection

TransPhrase can automatically detect the source language of your files:

- Samples text from your files to determine the dominant language
- Supports a wide range of languages including Chinese, Japanese, Korean, and more
- Detects language with high accuracy even from small text samples
- Falls back to user selection if detection fails
- Can be disabled with the `--no-auto-detect` flag

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

### Intelligent Text Chunking

TransPhrase uses semantic text chunking that:
- Respects sentence and paragraph boundaries
- Maintains context across chunks
- Optimizes chunk size for better translation quality
- Preserves document structure

### Plugin System

TransPhrase includes a flexible plugin system that allows you to extend functionality without modifying core code:

#### Types of Plugins

1. **Prompt Templates**: Customize the AI system prompt for different translation scenarios
   - Optimize translations for specific content types (novels, technical documentation, etc.)
   - Create genre-specific translation styles
   - Adapt to different writing conventions

2. **Processor Modules**: Modify text before or after translation
   - Ensure consistency in character names and terminology
   - Preserve formatting elements like code blocks
   - Apply content-specific post-processing

#### Using Plugins

Plugins are automatically discovered and presented during the configuration process:

```
Plugin Selection:
Do you want to use any plugins? (y/n) [n]: y

Available Prompt Templates:
1. NovelTranslationTemplate: Specialized template for translating novels
Use a custom prompt template? (y/n) [n]: y
Select prompt template [1]: 1

Available Processor Modules:
1. NameConsistencyProcessor: Maintains consistency of character names
Use text processor modules? (y/n) [n]: y
Select processor (0 to finish) [0]: 1
```

#### Creating Custom Plugins

TransPhrase automatically sets up plugin directories with examples:

```
~/.transphrase/plugins/
├── README.md                       # Plugin documentation
├── prompt_templates/               # Custom prompt templates
│   └── novel_template.py           # Example template
└── processors/                     # Text processor modules
    └── name_consistency.py         # Example processor
```

See the detailed documentation in [plugins.md](https://github.com/shinyPy/TransPhrase/blob/main/docs/plugins.md) for instructions on creating custom plugins.

## Usage Examples

### Basic Translation with Auto-Detection

```bash
# Create a sample Chinese file
echo "这是一个测试文件。它包含中文文本。" > ~/test-zh.txt

# Run TransPhrase with auto-detection
transphrase

# Follow prompts to select output directory
# The language will be automatically detected as Chinese
```

### Manual Language Selection

```bash
# Disable auto-detection if you want to manually specify the language
transphrase --no-auto-detect

# Follow prompts to select languages and other options
```

## Development
Please see [CONTRIBUTING](https://github.com/shinyPy/TransPhrase/blob/main/docs/CONTRIBUTING.md) for detailed information.

### CI/CD

TransPhrase uses GitHub Actions for continuous integration and deployment:
- Automatic testing on multiple Python versions (3.10+)
- Code quality checks (linting, formatting, type checking)
- Coverage reporting
- Automated releases to PyPI

## Requirements

- Python 3.10+
- OpenAI API key or compatible API endpoint

## License

TransPhrase is open-sourced software licensed under the MIT license.
