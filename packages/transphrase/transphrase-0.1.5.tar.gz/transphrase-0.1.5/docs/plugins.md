# TransPhrase Plugin System

TransPhrase provides a flexible plugin system that allows you to extend its functionality without modifying the core code. This document explains how to create and use plugins.

## Plugin Types

TransPhrase supports two types of plugins:

1. **Prompt Templates**: Customize the AI system prompt for different translation scenarios
2. **Processor Modules**: Modify text before or after translation

## Plugin Directory Structure

Plugins are stored in the following directory structure:

```
~/.transphrase/plugins/
├── README.md
├── prompt_templates/
│   └── novel_template.py
└── processors/
    └── name_consistency.py
```

## Creating a Prompt Template Plugin

Prompt templates allow you to customize the system prompt given to the AI model. This can help optimize translations for specific content types or styles.

Here's how to create a prompt template:

1. Create a new Python file in the `~/.transphrase/plugins/prompt_templates/` directory
2. Define a class that inherits from `PromptTemplate`
3. Implement the required methods

Example:

```python
from transphrase.plugins.plugin_manager import PromptTemplate

class TechnicalDocumentTemplate(PromptTemplate):
    """Specialized template for technical documentation translation"""

    @classmethod
    def get_system_prompt(cls) -> str:
        return """
You are a technical translator specializing in documentation.
Translate the following text from {source_language} to {target_language}.

Guidelines:
1. Maintain precise technical terminology
2. Keep formatting intact (lists, code blocks, etc.)
3. Preserve all numerical values and units
4. Maintain consistent terminology throughout
5. Use industry-standard terminology in {target_language}

Output only the translated text with no additional commentary.
"""
```

## Creating a Processor Module Plugin

Processor modules can modify text before or after translation, allowing for custom text processing.

Here's how to create a processor:

1. Create a new Python file in the `~/.transphrase/plugins/processors/` directory
2. Define a class that inherits from `ProcessorModule`
3. Implement the `process_text` method

Example:

```python
from transphrase.plugins.plugin_manager import ProcessorModule

class CodeBlockPreserver(ProcessorModule):
    """Preserves code blocks during translation"""

    def __init__(self):
        self.code_blocks = []

    def process_text(self, text: str) -> str:
        """Process text to protect and restore code blocks"""
        import re

        # Extract code blocks and replace with placeholders
        pattern = r'```[\w]*\n(.*?)```'

        def replace_code(match):
            self.code_blocks.append(match.group(0))
            return f"CODE_BLOCK_{len(self.code_blocks)}"

        processed = re.sub(pattern, replace_code, text, flags=re.DOTALL)

        # At this point, translation would happen in the main system

        # Restore code blocks
        for i, block in enumerate(self.code_blocks, 1):
            processed = processed.replace(f"CODE_BLOCK_{i}", block)

        return processed
```

## Using Plugins

When running TransPhrase, you'll be prompted to select plugins if any are available:

```
Plugin Selection:
Do you want to use any plugins? (y/n) [n]: y

Available Prompt Templates:
1. NovelTranslationTemplate: Specialized template for translating novels with character and terminology tracking
Use a custom prompt template? (y/n) [n]: y
Select prompt template [1]: 1

Available Processor Modules:
1. NameConsistencyProcessor: Maintains consistency of character names across translations
Use text processor modules? (y/n) [n]: y
Select processor (0 to finish) [0]: 1
Selected processors: NameConsistencyProcessor
Select processor (0 to finish) [0]: 0
```

## Plugin Configuration in config.json

If you save your configuration, plugin selections will be stored in your config.json file:

```json
{
  "api_key": "your-api-key",
  "base_url": "https://api.electronhub.top",
  "model": "deepseek-llm-67b-chat",
  "mode": "translate",
  "source_language": "Chinese",
  "target_language": "English",
  "source_dir": "/path/to/source",
  "output_dir": "/path/to/output",
  "skip_existing": true,
  "workers": 4,
  "use_cache": true,
  "cache_ttl": 86400,
  "db_path": "~/.transphrase/transphrase.db",
  "plugins": {
    "prompt_template": "NovelTranslationTemplate",
    "processors": ["NameConsistencyProcessor"]
  }
}
```

## Best Practices for Plugin Development

1. **Error Handling**: Include proper error handling in your plugins
2. **Documentation**: Add clear docstrings to your plugin classes
3. **Testing**: Test your plugins with various input scenarios
4. **Compatibility**: Ensure your plugins work with both translation and polish modes
5. **Performance**: Keep processor modules efficient, especially for large texts

## Plugin Limitations

- Plugins do not have access to TransPhrase's internal cache or database
- Processor modules run sequentially in the order they were selected
- Currently, only Python plugins are supported
