# Django Project Scrubber

A powerful tool to analyze Django projects for unused components, helping you keep your codebase clean and maintainable.

## Features

- Identifies potentially unused URLs
- Finds unused methods (coming soon)
- Detects duplicate method implementations (coming soon)
- Identifies unused templates

## Installation

```bash
pip install django-project-scrubber
```

## Usage

To analyze a Django project, run:

```bash
django_scrubber /path/to/your/django/project
```

The tool will analyze your project and display a summary of findings, including:
- Potentially unused URLs (excluding admin and auth URLs)
- Unused methods (coming in future versions)
- Duplicate method implementations (coming in future versions)
- Unused templates (including analysis of includes, extends, and view usage)

## Example Output

```
Django Project Analysis Summary
==============================

Potentially Unused URLs:
- /api/v1/old-endpoint/ (name: api:old_endpoint)
- /legacy/dashboard/ (name: legacy:dashboard)
- /unused-feature/ (name: unused_feature)

Unused Templates:
- templates/old_feature.html
- templates/legacy/header.html

Note: This is a static analysis and may have false positives.
Please verify these results before making any changes.
```

## How It Works

The Django Project Scrubber analyzes your Django project by:
1. Scanning all URL patterns in your project
2. Checking URL usage in templates and code
3. Analyzing template usage (includes, extends, and view rendering)
4. Filtering out common false positives (admin, auth, etc.)
5. Providing a clear summary of potentially unused components

## Requirements

- Python 3.8 or higher
- Django 3.0 or higher

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Author

HappyMinsker - [GitHub](https://github.com/HappyMinsker)

## Project Status

This is version 0.1.1 with URL and template analysis functionality. More features are planned for future releases. 