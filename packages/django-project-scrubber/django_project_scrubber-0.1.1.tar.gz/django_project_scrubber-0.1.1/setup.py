from setuptools import setup, find_packages

setup(
    name="django-project-scrubber",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "Django>=3.0",
        "click>=8.0",
    ],
    entry_points={
        "console_scripts": [
            "django_scrubber=DjangoScrubber.DjangoScrubber:main",
        ],
    },
    author="HappyMinsker",
    author_email="daniit.system@gmail.com",
    description="A tool to analyze Django projects for unused components",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HappyMinsker/DjangoScrubber",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
) 