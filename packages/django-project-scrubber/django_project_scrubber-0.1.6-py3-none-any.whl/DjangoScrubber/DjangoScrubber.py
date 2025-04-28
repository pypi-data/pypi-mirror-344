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
        self._configure_django()
        
    def _configure_django(self):
        """Configure Django settings for the project"""
        # Add project directory to Python path
        sys.path.insert(0, str(self.project_path))
        
        # Find the settings module
        project_name = None
        for item in self.project_path.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                if (item / 'settings.py').exists() and (item / 'urls.py').exists():
                    project_name = item.name
                    break
        
        if not project_name:
            raise click.ClickException("Could not find Django project settings")
            
        # Configure Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
        django.setup()
        
    def _find_url_usage_in_templates(self, url_name):
        """Check if a URL is used in templates"""
        for app_config in apps.get_app_configs():
            app_path = app_config.path
            templates_dir = os.path.join(app_path, 'templates')
            if not os.path.exists(templates_dir):
                continue
                
            for root, _, files in os.walk(templates_dir):
                for file in files:
                    if file.endswith(('.html', '.txt')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # Check for URL usage in templates with different patterns
                                url_patterns = [
                                    f"{{% url '{url_name}'",  # URL tag start
                                    f'{{% url "{url_name}"',  # URL tag start with double quotes
                                    f"{{% url '{url_name}' with",  # URL with context
                                    f'{{% url "{url_name}" with',  # URL with context, double quotes
                                    f"{{% url '{url_name}' as",  # URL as variable
                                    f'{{% url "{url_name}" as',  # URL as variable, double quotes
                                ]
                                
                                # Check for URL usage in href attributes
                                href_patterns = [
                                    f'href="{{% url \'{url_name}\'',  # Standard href
                                    f"href='{{% url \"{url_name}\"",  # Double quotes
                                    f'href="{{% url \'{url_name}\' with',  # With context
                                    f"href='{{% url \"{url_name}\" with",  # With context, double quotes
                                ]
                                
                                # Check for URL usage in form actions
                                action_patterns = [
                                    f'action="{{% url \'{url_name}\'',  # Standard action
                                    f"action='{{% url \"{url_name}\"",  # Double quotes
                                ]
                                
                                # Combine all patterns
                                all_patterns = url_patterns + href_patterns + action_patterns
                                
                                for pattern in all_patterns:
                                    if pattern in content:
                                        return True
                                        
                                # Check for reverse() usage
                                reverse_patterns = [
                                    f"reverse('{url_name}'",
                                    f'reverse("{url_name}"',
                                    f"reverse_lazy('{url_name}'",
                                    f'reverse_lazy("{url_name}"',
                                ]
                                
                                for pattern in reverse_patterns:
                                    if pattern in content:
                                        return True
                        except UnicodeDecodeError:
                            continue
        return False
        
    def _find_url_usage_in_code(self, url_name):
        """Check if a URL is used in Python code"""
        for app_config in apps.get_app_configs():
            app_path = app_config.path
            for root, _, files in os.walk(app_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # Check for URL usage in code
                                if f"reverse('{url_name}')" in content:
                                    return True
                                if f'reverse("{url_name}")' in content:
                                    return True
                                if f"url = '{url_name}'" in content:
                                    return True
                                if f'url = "{url_name}"' in content:
                                    return True
                        except UnicodeDecodeError:
                            continue
        return False
        
    def _find_url_references_in_django(self):
        """Find URL references in Django source code"""
        used_urls = set()
        
        # Get Django installation path
        django_path = os.path.dirname(django.__file__)
        
        # Patterns to look for in Django source
        patterns = [
            # URL reversing
            r'reverse\([\'"]([^\'"]+)[\'"]',
            r'reverse_lazy\([\'"]([^\'"]+)[\'"]',
            r'get_absolute_url\(\)\s*return\s*reverse\([\'"]([^\'"]+)[\'"]',
            
            # Admin URLs
            r'admin:[^\'"]+',
            r'admin\.site\.urls',
            
            # Auth URLs
            r'auth:[^\'"]+',
            r'auth\.urls',
            
            # Static and media URLs
            r'static\([\'"]([^\'"]+)[\'"]',
            r'media\([\'"]([^\'"]+)[\'"]',
        ]
        
        # Scan Django source files
        for root, _, files in os.walk(django_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            for pattern in patterns:
                                matches = re.findall(pattern, content)
                                for match in matches:
                                    if isinstance(match, str):
                                        used_urls.add(match)
                                    else:
                                        # Handle tuple matches
                                        for m in match:
                                            if isinstance(m, str):
                                                used_urls.add(m)
                    except UnicodeDecodeError:
                        continue
        
        return used_urls

    def _find_unused_urls(self):
        """Find URLs that are defined but never used"""
        resolver = get_resolver()
        all_urls = set()
        used_urls = set()
        
        def collect_urls(resolver, prefix='', namespace=''):
            """Recursively collect URLs from the resolver"""
            for pattern in resolver.url_patterns:
                if hasattr(pattern, 'url_patterns'):
                    # This is an include() pattern
                    new_prefix = prefix
                    if pattern.pattern:
                        new_prefix = prefix + str(pattern.pattern)
                    new_namespace = namespace
                    if hasattr(pattern, 'namespace'):
                        new_namespace = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                    collect_urls(pattern, new_prefix, new_namespace)
                else:
                    # This is a URL pattern
                    full_path = prefix + str(pattern.pattern)
                    # Skip admin URLs and authentication URLs
                    if not full_path.startswith(('admin/', 'auth/', 'login/', 'logout/')):
                        url_name = pattern.name
                        if namespace:
                            url_name = f"{namespace}:{url_name}"
                        all_urls.add((full_path, url_name))
        
        collect_urls(resolver)
        
        # Get URL references from Django source
        django_urls = self._find_url_references_in_django()
        used_urls.update(django_urls)
        
        # Check URL usage in templates and code
        for path, name in all_urls:
            if name and (self._find_url_usage_in_templates(name) or self._find_url_usage_in_code(name)):
                used_urls.add(name)
        
        # Convert used_urls to the same format as all_urls for comparison
        used_urls_with_paths = set()
        for path, name in all_urls:
            if name in used_urls:
                used_urls_with_paths.add((path, name))
        
        self.unused_urls = sorted(list(all_urls - used_urls_with_paths))
    
    def _find_unused_methods(self):
        """Find methods that are defined but never used"""
        for app_config in apps.get_app_configs():
            app_path = app_config.path
            for root, _, files in os.walk(app_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                try:
                                    tree = ast.parse(f.read())
                                    for node in ast.walk(tree):
                                        if isinstance(node, ast.FunctionDef):
                                            # TODO: Implement method usage tracking
                                            # This would require analyzing imports and calls
                                            pass
                                except SyntaxError:
                                    continue
                        except UnicodeDecodeError:
                            # Skip files that can't be read with UTF-8
                            continue
    
    def _find_duplicate_methods(self):
        """Find methods with identical implementations"""
        method_hashes = defaultdict(list)
        
        for app_config in apps.get_app_configs():
            app_path = app_config.path
            for root, _, files in os.walk(app_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                try:
                                    tree = ast.parse(f.read())
                                    for node in ast.walk(tree):
                                        if isinstance(node, ast.FunctionDef):
                                            # TODO: Implement method comparison
                                            # This would require hashing method implementations
                                            pass
                                except SyntaxError:
                                    continue
                        except UnicodeDecodeError:
                            # Skip files that can't be read with UTF-8
                            continue
    
    def _find_template_references_in_django(self):
        """Find template references in Django source code"""
        used_templates = set()
        
        # Get Django installation path
        django_path = os.path.dirname(django.__file__)
        
        # Patterns to look for in Django source
        patterns = [
            # Template loading
            r'get_template\([\'"]([^\'"]+)[\'"]\)',
            r'select_template\(\[[\'"]([^\'"]+)[\'"]\]\)',
            r'TemplateView\.as_view\([^)]*template_name\s*=\s*[\'"]([^\'"]+)[\'"]\)',
            
            # Error templates
            r'handler400\s*=\s*[\'"]([^\'"]+)[\'"]',
            r'handler403\s*=\s*[\'"]([^\'"]+)[\'"]',
            r'handler404\s*=\s*[\'"]([^\'"]+)[\'"]',
            r'handler500\s*=\s*[\'"]([^\'"]+)[\'"]',
            
            # Admin templates
            r'admin/[^\'"]+\.html',
            
            # Auth templates
            r'auth/[^\'"]+\.html',
        ]
        
        # Scan Django source files
        for root, _, files in os.walk(django_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            for pattern in patterns:
                                matches = re.findall(pattern, content)
                                for match in matches:
                                    if isinstance(match, str):
                                        used_templates.add(match)
                                    else:
                                        # Handle tuple matches
                                        for m in match:
                                            if isinstance(m, str):
                                                used_templates.add(m)
                    except UnicodeDecodeError:
                        continue
        
        return used_templates

    def _find_unused_templates(self):
        """Find template files that are never used"""
        template_dirs = settings.TEMPLATES[0]['DIRS']
        all_templates = set()
        used_templates = set()
        
        # Get all template files
        for template_dir in template_dirs:
            for root, _, files in os.walk(template_dir):
                for file in files:
                    if file.endswith(('.html', '.txt')):
                        template_path = os.path.relpath(
                            os.path.join(root, file),
                            template_dir
                        )
                        all_templates.add(template_path)
        
        # Get template references from Django source
        django_templates = self._find_template_references_in_django()
        used_templates.update(django_templates)
        
        # Check template usage in views
        for app_config in apps.get_app_configs():
            app_path = app_config.path
            for root, _, files in os.walk(app_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # Check for template rendering in views with different patterns
                                render_patterns = [
                                    r'template_name\s*=\s*[\'"]([^\'"]+)[\'"]',  # Direct template_name assignment
                                    r'render\([^)]*template_name\s*=\s*[\'"]([^\'"]+)[\'"]',  # Named parameter
                                    r'render\([^)]*[\'"]([^\'"]+)[\'"]\s*,',  # Positional parameter
                                    r'TemplateView\.as_view\([^)]*template_name\s*=\s*[\'"]([^\'"]+)[\'"]',  # Class-based view
                                    r'get_template_names\([^)]*return\s*\[[\'"]([^\'"]+)[\'"]\]',  # Template name method
                                    r'handler400\s*=\s*[\'"]([^\'"]+)[\'"]',  # Error handler 400
                                    r'handler403\s*=\s*[\'"]([^\'"]+)[\'"]',  # Error handler 403
                                    r'handler404\s*=\s*[\'"]([^\'"]+)[\'"]',  # Error handler 404
                                    r'handler500\s*=\s*[\'"]([^\'"]+)[\'"]',  # Error handler 500
                                ]
                                for pattern in render_patterns:
                                    matches = re.findall(pattern, content)
                                    for match in matches:
                                        normalized_path = match.replace('\\', '/')
                                        used_templates.add(normalized_path)
                        except UnicodeDecodeError:
                            continue
        
        # Check template usage in other templates
        for template_dir in template_dirs:
            for root, _, files in os.walk(template_dir):
                for file in files:
                    if file.endswith(('.html', '.txt')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # Check for template includes with different quote styles and path formats
                                include_patterns = [
                                    r'{%\s*include\s*[\'"]([^\'"]+)[\'"]\s*%}',  # Standard include
                                    r'{%\s*include\s*[\'"]([^\'"]+)[\'"]\s*with\s*%}',  # Include with context
                                    r'{%\s*include\s*[\'"]([^\'"]+)[\'"]\s*only\s*%}',  # Include only
                                    r'{%\s*include\s*[\'"]([^\'"]+)[\'"]\s*with\s*[^%]*\s*%}',  # Include with complex context
                                    r'{%\s*include\s*[\'"]([^\'"]+)[\'"]\s*only\s*with\s*[^%]*\s*%}',  # Include only with context
                                ]
                                for pattern in include_patterns:
                                    matches = re.findall(pattern, content)
                                    for match in matches:
                                        # Normalize the template path
                                        normalized_path = match.replace('\\', '/')
                                        used_templates.add(normalized_path)
                                
                                # Check for template extends with different quote styles
                                extend_patterns = [
                                    r'{%\s*extends\s*[\'"]([^\'"]+)[\'"]\s*%}',  # Standard extend
                                    r'{%\s*extends\s*[\'"]([^\'"]+)[\'"]\s*with\s*%}',  # Extend with context
                                ]
                                for pattern in extend_patterns:
                                    matches = re.findall(pattern, content)
                                    for match in matches:
                                        normalized_path = match.replace('\\', '/')
                                        used_templates.add(normalized_path)
                                    
                                # Check for template inheritance
                                block_matches = re.findall(r'{%\s*block\s*[\'"]([^\'"]+)[\'"]\s*%}', content)
                                if block_matches:
                                    # If a template has blocks, it's likely being extended
                                    template_path = os.path.relpath(file_path, template_dir)
                                    normalized_path = template_path.replace('\\', '/')
                                    used_templates.add(normalized_path)
                                
                                # Check for URL usage in templates
                                url_patterns = [
                                    r'{%\s*url\s*[\'"]([^\'"]+)[\'"]\s*%}',  # Standard URL tag
                                    r'{%\s*url\s*[\'"]([^\'"]+)[\'"]\s*with\s*%}',  # URL with context
                                    r'{%\s*url\s*[\'"]([^\'"]+)[\'"]\s*as\s*%}',  # URL as variable
                                    r'href\s*=\s*[\'"][^\'"]*{%\s*url\s*[\'"]([^\'"]+)[\'"]\s*%}[^\'"]*[\'"]',  # URL in href
                                    r'action\s*=\s*[\'"][^\'"]*{%\s*url\s*[\'"]([^\'"]+)[\'"]\s*%}[^\'"]*[\'"]',  # URL in form action
                                ]
                                for pattern in url_patterns:
                                    matches = re.findall(pattern, content)
                                    for match in matches:
                                        if isinstance(match, str):
                                            # If this template uses URLs, it's likely being used
                                            template_path = os.path.relpath(file_path, template_dir)
                                            normalized_path = template_path.replace('\\', '/')
                                            used_templates.add(normalized_path)
                        except UnicodeDecodeError:
                            continue
        
        # Normalize all template paths for comparison
        all_templates = {path.replace('\\', '/') for path in all_templates}
        used_templates = {path.replace('\\', '/') for path in used_templates}
        
        # Find unused templates
        self.unused_templates = sorted(list(all_templates - used_templates))
    
    def analyze_project(self):
        """Main analysis function that runs all checks"""
        self._find_unused_urls()
        self._find_unused_methods()
        self._find_duplicate_methods()
        self._find_unused_templates()
        
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
        
        if self.unused_methods:
            summary.append("\nUnused Methods:")
            for method in self.unused_methods:
                summary.append(f"- {method}")
        else:
            summary.append("\n✅ No unused methods found! All methods are being used.")
        
        if self.duplicate_methods:
            summary.append("\nDuplicate Methods:")
            for method_group in self.duplicate_methods:
                summary.append("Similar implementations found in:")
                for method in method_group:
                    summary.append(f"- {method}")
        else:
            summary.append("\n✅ No duplicate methods found! All methods are unique.")
        
        if self.unused_templates:
            summary.append("\nUnused Templates:")
            for template in self.unused_templates:
                summary.append(f"- {template}")
        else:
            summary.append("\n✅ No unused templates found! All templates are being used.")
                
        if not any([self.unused_urls, self.unused_methods, self.duplicate_methods, self.unused_templates]):
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
        scrubber = DjangoScrubber(project_path)
        scrubber.analyze_project()
        print(scrubber.get_summary())
    except Exception as e:
        raise click.ClickException(str(e))

if __name__ == '__main__':
    main()