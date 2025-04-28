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
        self.excluded_dirs = ['static', 'staticfiles', 'media', '.git', 'node_modules', 'venv', 'migrations', 
                              '.cursor']

    def _should_exclude_path(self, path):
        """Check if the path should be excluded from analysis"""
        path_str = str(path)
        return any(excluded_dir in path_str for excluded_dir in self.excluded_dirs)

    def _find_all_templates(self):
        """Find all template files in the project"""
        templates = set()
        for root, _, files in os.walk(self.project_path):
            if self._should_exclude_path(root):
                continue
            for file in files:
                if file.endswith(('.html', )):
                    templates.add(os.path.join(root, file))
        return templates

    def _find_template_usage(self, template_path):
        """Check if a template is used anywhere in the project"""
        template_name = os.path.basename(template_path)
        
        # Get relative path from templates directory
        templates_index = template_path.find('templates')
        if templates_index != -1:
            relative_path = template_path[templates_index + len('templates') + 1:]
        else:
            relative_path = template_name
        
        for root, _, files in os.walk(self.project_path):
            if self._should_exclude_path(root):
                continue
            for file in files:
                if file.endswith(('.py', '.html')):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            # Look for the template name or path in any context
                            if template_name in content or relative_path in content:
                                return True
                                        
                    except UnicodeDecodeError:
                        continue
        return False

    def _find_all_urls(self):
        """Find all URL patterns in urls.py files"""
        urls = []
        for root, _, files in os.walk(self.project_path):
            if self._should_exclude_path(root):
                continue
            if 'urls.py' in files:
                try:
                    urls_file = os.path.join(root, 'urls.py')
                    print(f"Analyzing URLs in: {urls_file}")
                    with open(urls_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Find app_name if present
                        app_name_match = re.search(r"app_name\s*=\s*['\"]([^'\"]+)['\"]", content)
                        namespace = app_name_match.group(1) if app_name_match else None
                        
                        # Find URL patterns and names
                        patterns = re.findall(r"path\(['\"]([^'\"]+)['\"]", content)
                        names = re.findall(r"name=['\"]([^'\"]+)['\"]", content)
                        
                        # Add URLs with namespace if present
                        found_urls = list(zip(patterns, names))
                        for pattern, name in found_urls:
                            if namespace:
                                urls.append((pattern, f"{namespace}:{name}"))
                            else:
                                urls.append((pattern, name))
                        
                        # Display found URLs count
                        if found_urls:
                            print(f"  - Found {len(found_urls)} URLs:")
                        else:
                            print("  - No URLs found in this file")
                except UnicodeDecodeError:
                    print(f"  Could not read file (encoding issue): {urls_file}")
                    continue
                except Exception as e:
                    print(f"  Error processing file {urls_file}: {str(e)}")
                    continue
        return urls

    def _find_urls_in_file(self, file_path):
        """Helper method to find URLs in a specific urls.py file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                patterns = re.findall(r"path\(['\"]([^'\"]+)['\"]", content)
                names = re.findall(r"name=['\"]([^'\"]+)['\"]", content)
                return list(zip(patterns, names))
        except:
            return []

    def _find_url_usage_in_html(self, url_name):
        """Check if a URL name is used in HTML templates"""
        found_usage = False
        
        # Get just the name part (after the last colon if there is one)
        name = url_name.split(':')[-1]
        
        for root, _, files in os.walk(self.project_path):
            if self._should_exclude_path(root):
                continue
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            # Look for the URL name in any context within template tags
                            if f"url '{name}'" in content or f'url "{name}"' in content:
                                found_usage = True
                                break
                                
                            # Also check for the full URL name
                            if f"url '{url_name}'" in content or f'url "{url_name}"' in content:
                                found_usage = True
                                break
                                
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        continue
            if found_usage:
                break
        return found_usage

    def analyze_project(self):
        """Main analysis function that runs all checks"""
        print("\nFinding unused URLs...\n")
        all_urls = self._find_all_urls()
        found_urls = []
        for path, name in all_urls:
            # Check both the full URL name and just the name part (for namespaced URLs)
            if self._find_url_usage_in_html(name) or self._find_url_usage_in_html(name.split(':')[-1]):
                found_urls.append(name)
        self.unused_urls = [(path, name) for path, name in all_urls if name not in found_urls]

        print("\nFinding unused templates...")
        all_templates = self._find_all_templates()
        self.unused_templates = [str(t) for t in all_templates if not self._find_template_usage(t)]

    def get_summary(self):
        """Return a formatted summary of findings"""
        summary = []
        summary.append("Django Project Analysis Summary")
        summary.append("=" * 30)
        
        if self.unused_urls:
            summary.append(f"\nPotentially Unused URLs ({len(self.unused_urls)}):")
            for path, name in self.unused_urls:
                summary.append(f"- {path} (name: {name})")
        else:
            summary.append("\n✅ No unused URLs found! All URLs are being used.")

        if self.unused_templates:
            summary.append(f"\nUnused Templates ({len(self.unused_templates)}):")
            # Sort the templates by their path
            sorted_templates = sorted(self.unused_templates)
            for template in sorted_templates:
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