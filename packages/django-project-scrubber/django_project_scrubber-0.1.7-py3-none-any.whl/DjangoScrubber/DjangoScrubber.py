# mypackage/mypackage.py
def greet(name):
    return f"Hello, {name}!"

import os
import ast
import sys
import re
from collections import defaultdict
from pathlib import Path
import django
from django.conf import settings
from django.urls import get_resolver, reverse
from django.template.loader import get_template
from django.apps import apps
import click

class DjangoScrubber:
    def __init__(self, project_path):
        self.project_path = Path(project_path).resolve()
        self.unused_urls = []
        self.unused_methods = []
        self.duplicate_methods = []
        self.unused_templates = []

    def _find_all_templates(self):
        """Find all template files in the project"""
        templates = set()
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(('.html', '.txt')):
                    templates.add(os.path.join(root, file))
        return templates

    def _find_template_usage(self, template_path):
        """Check if a template is used anywhere in the project"""
        template_name = os.path.basename(template_path)
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(('.py', '.html')):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Check for template usage in Python files
                            if file.endswith('.py'):
                                if f"'{template_name}'" in content or f'"{template_name}"' in content:
                                    return True
                            # Check for template usage in other templates
                            elif file.endswith('.html'):
                                patterns = [
                                    f'{{% extends "{template_name}" %}}',
                                    f"{{% extends '{template_name}' %}}",
                                    f'{{% include "{template_name}" %}}',
                                    f"{{% include '{template_name}' %}}",
                                ]
                                for pattern in patterns:
                                    if pattern in content:
                                        return True
                    except UnicodeDecodeError:
                        continue
        return False

    def _find_all_urls(self):
        """Find all URL patterns in urls.py files"""
        urls = []
        for root, _, files in os.walk(self.project_path):
            if 'urls.py' in files:
                try:
                    with open(os.path.join(root, 'urls.py'), 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Find URL patterns
                        patterns = re.findall(r"path\(['\"]([^'\"]+)['\"]", content)
                        names = re.findall(r"name=['\"]([^'\"]+)['\"]", content)
                        urls.extend(list(zip(patterns, names)))
                except UnicodeDecodeError:
                    continue
        return urls

    def _find_url_usage(self, url_name):
        """Check if a URL name is used anywhere in the project"""
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(('.py', '.html')):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Check for URL usage in Python files
                            if file.endswith('.py'):
                                if f"reverse('{url_name}')" in content or f'reverse("{url_name}")' in content:
                                    return True
                            # Check for URL usage in templates
                            elif file.endswith('.html'):
                                patterns = [
                                    f'{{% url "{url_name}" %}}',
                                    f"{{% url '{url_name}' %}}",
                                    f'href="{{% url "{url_name}" %}}"',
                                    f"href='{{% url '{url_name}' %}}'"
                                ]
                                for pattern in patterns:
                                    if pattern in content:
                                        return True
                    except UnicodeDecodeError:
                        continue
        return False

    def analyze_project(self):
        """Main analysis function that runs all checks"""
        print("Finding unused URLs...")
        all_urls = self._find_all_urls()
        self.unused_urls = [(path, name) for path, name in all_urls if not self._find_url_usage(name)]

        print("Finding unused templates...")
        all_templates = self._find_all_templates()
        self.unused_templates = [str(t) for t in all_templates if not self._find_template_usage(t)]

    def get_summary(self):
        """Return a formatted summary of findings"""
        summary = []
        summary.append("Django Project Analysis Summary")
        summary.append("=" * 30)
        
        if self.unused_urls:
            summary.append("\nPotentially Unused URLs:")
            for path, name in self.unused_urls:
                summary.append(f"- {path} (name: {name})")
        else:
            summary.append("\n✅ No unused URLs found! All URLs are being used.")

        if self.unused_templates:
            summary.append("\nUnused Templates:")
            for template in self.unused_templates:
                summary.append(f"- {template}")
        else:
            summary.append("\n✅ No unused templates found! All templates are being used.")
                
        if not any([self.unused_urls, self.unused_templates]):
            summary.append("\n🎉 Great news! Your Django project is clean and well-maintained.")
            summary.append("No unused components were found in your codebase.")
        else:
            summary.append("\nNote: This is a static analysis and may have false positives.")
            summary.append("Please verify these results before making any changes.")
        
        return "\n".join(summary)

@click.command()
@click.argument('project_path', type=click.Path(exists=True))
def main(project_path):
    """Analyze a Django project for unused components."""
    try:
        print(f"Analyzing project at: {project_path}")
        scrubber = DjangoScrubber(project_path)
        scrubber.analyze_project()
        print("\n" + scrubber.get_summary())
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        raise click.ClickException(str(e))

if __name__ == '__main__':
    main()