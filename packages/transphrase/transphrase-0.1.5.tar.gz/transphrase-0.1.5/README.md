# TransPhrase
### Version 0.1.5 (ALPHA) ⚠️ .

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
- HTML processing with structure preservation
- Batch translation with stable delimiters
- Robust error handling and recovery mechanisms
- Advanced context tracking for more consistent translations

## Project Structure

The TransPhrase project is organized into several core modules:

```
transphrase/
├── api/               # API handlers and client implementations
├── cache/             # Translation caching and context management
├── cli/               # Command-line interface implementation
├── core/              # Core processing logic and configuration
├── database/          # Database models and operations
├── formats/           # File format handlers and processors
├── models/            # Language model implementations
├── plugins/           # Plugin system implementation
├── rate_limiting/     # Rate limiting and API quota management
└── ui/                # User interface components
```

Each module is designed to be independently testable and maintainable, with clear separation of concerns.

## Operation Modes

TransPhrase supports two operation modes:

### Translation Mode

Converts text between different languages while maintaining tone, style, and meaning.

- Perfect for web novels, technical documents, or any text content
- Preserves character names, terms, and stylistic elements
- Optimized for context-aware translation across multiple files
- HTML structure preservation for web content

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
  "auto_detect_language": true,
  "polish_style": "natural"
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
- Enhanced caching with glossary term application

### Intelligent Text Chunking

TransPhrase uses semantic text chunking that:
- Respects sentence and paragraph boundaries
- Maintains context across chunks
- Optimizes chunk size for better translation quality
- Preserves document structure

### HTML Processing

- Preserves document structure and formatting during translation
- Maintains HTML tags, attributes, and nested elements
- Handles special cases like `select`/`option` elements properly
- Processes large HTML files efficiently with streaming techniques
- Ensures valid HTML output through structure validation and recovery

### Batch Translation

- Stable, UUID-based delimiters for consistent batch processing
- Robust handling of API responses that don't maintain delimiters
- Graceful fallback to individual translation when needed
- Efficient caching of batch results for improved performance

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
transphrase translate process-files

# Follow prompts to select output directory
# The language will be automatically detected as Chinese
```

### Manual Language Selection

```bash
# Disable auto-detection if you want to manually specify the language
transphrase translate process-files --no-auto-detect

# Follow prompts to select languages and other options
```

### Translating HTML Content

```bash
# Run TransPhrase with HTML files in your source directory
transphrase

# HTML files will be processed with special handling to preserve structure
```

## Development

The project follows test-driven development practices with comprehensive test coverage. The test suite includes:

```
tests/
├── __init__.py
├── test_api_handler.py       # API handler tests
├── test_basic.py             # Basic functionality tests
├── test_cache.py             # Cache system tests
├── test_config.py            # Configuration tests
├── test_config_validator.py  # Config validation tests
├── test_database.py          # Database operation tests
├── test_file_processor.py    # File processing tests
├── test_glossary.py          # Glossary and terminology tests
├── test_html_processor.py    # HTML processing tests
├── test_integration.py       # Integration tests
├── test_model_selector.py    # Model selection tests
├── test_rate_limiter.py      # Rate limiting tests
```

### Testing Guidelines

- Unit tests should cover all core functionality
- Integration tests verify module interactions
- Tests are run automatically on every commit via CI/CD
- Code coverage is maintained above 90%
- Mocking is used extensively for external dependencies

Please see [CONTRIBUTING](https://github.com/shinyPy/TransPhrase/blob/main/docs/CONTRIBUTING.md) for detailed development guidelines.

### CI/CD

TransPhrase uses GitHub Actions for continuous integration and deployment:
- Automatic testing on multiple Python versions (3.10+)
- Code quality checks (linting, formatting, type checking)
- Coverage reporting
- Automated releases to PyPI

## Requirements

### System Requirements

- Python 3.10 or higher
- 4GB RAM minimum (8GB recommended)
- 500MB disk space
- Internet connection for API access

### Python Dependencies

Core dependencies (automatically installed):
- requests >= 2.31.0
- tqdm >= 4.66.1
- pydantic >= 2.5.0
- sqlalchemy >= 2.0.0
- python-dotenv >= 1.0.0
- beautifulsoup4 >= 4.12.0
- rich >= 13.0.0

## Changelog

### Version 0.1.5 (ALPHA)
- Added robust HTML processing with structure preservation
- Improved batch translation with stable UUID-based delimiters
- Enhanced error handling and recovery throughout the application
- Added quality assessment improvements for more consistent evaluations
- Fixed various bugs affecting HTML and text processing
- Added comprehensive testing for HTML processing components

### Version 0.1.0 (ALPHA)
- Initial release with basic functionality
- Translation and polish modes
- Support for multiple languages and models
- File processing and caching system
- Database integration for tracking translation jobs
