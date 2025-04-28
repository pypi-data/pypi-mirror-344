# Django Project Scrubber

A tool to analyze Django projects for unused components, helping you keep your codebase clean and maintainable.

## Features

- 🔍 Find unused URLs in your Django project
- 📄 Identify unused templates
- 🔄 Detect duplicate method names
- 🧹 Clean up unused code
- 🚀 Improved URL detection with support for namespaced URLs
- 📝 Enhanced template analysis with dynamic scanning
- 🎯 Better console output with positive messages
- 🔧 Support for Python 3.8 through 3.11

## Installation

```bash
pip install django-project-scrubber
```

## Usage

```bash
django_scrubber /path/to/your/django/project
```

## Project Status

Version 0.1.7 - Enhanced URL and template analysis with improved detection patterns and better console output.

## License

MIT License

## Author

HappyMinsker - [GitHub](https://github.com/HappyMinsker)

## How It Works

The Django Project Scrubber analyzes your Django project by:
1. Scanning URL patterns in urls.py files
2. Checking URL usage in templates by looking for URL names in template tags
3. Analyzing template usage by searching for template names in Python files and other templates
4. Supporting partial templates (files starting with underscore)
5. Providing a summary of potentially unused URLs and templates

Note: This is a static analysis tool and may have false positives. It's recommended to:
- Review the results carefully before making any changes
- Consider that some URLs might be used dynamically or through JavaScript
- Some templates might be used in ways not detected by the tool
- Check for any custom URL resolution or template loading mechanisms in your project

## Requirements

- Python 3.8 or higher
- Django 3.0 or higher

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 