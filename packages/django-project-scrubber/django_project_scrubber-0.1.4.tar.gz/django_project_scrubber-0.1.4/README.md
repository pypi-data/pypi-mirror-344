# Django Project Scrubber

A powerful tool to analyze Django projects for unused components, helping you keep your codebase clean and maintainable.

## Features

- Identifies potentially unused URLs (including namespaced URLs and Django built-in URLs)
- Finds unused methods (coming soon)
- Detects duplicate method implementations (coming soon)
- Identifies unused templates (with improved include/extends detection and Django template analysis)
- Supports partial templates (files starting with underscore)
- Enhanced URL detection in templates (including href attributes and form actions)

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

✅ No unused URLs found! All URLs are being used.

✅ No unused methods found! All methods are being used.

✅ No duplicate methods found! All methods are unique.

✅ No unused templates found! All templates are being used.

🎉 Great news! Your Django project is clean and well-maintained.
No unused components were found in your codebase.
```

## How It Works

The Django Project Scrubber analyzes your Django project by:
1. Scanning all URL patterns in your project
2. Checking URL usage in templates and code (including namespaced URLs)
3. Analyzing Django source code for built-in URL and template usage
4. Analyzing template usage (includes, extends, and view rendering)
5. Supporting partial templates (files starting with underscore)
6. Detecting URLs in template attributes (href, form actions)
7. Filtering out common false positives (admin, auth, etc.)
8. Providing a clear summary of potentially unused components

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

This is version 0.1.4 with improved template and URL analysis functionality, including support for partial templates and enhanced URL detection in template attributes. More features are planned for future releases. 