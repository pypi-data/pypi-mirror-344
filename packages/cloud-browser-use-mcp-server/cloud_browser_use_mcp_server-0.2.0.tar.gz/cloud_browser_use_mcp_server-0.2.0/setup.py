from setuptools import setup, find_packages

setup(
    name="cloud-browser-use-mcp-server",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
        "httpx>=0.24.0",
        "click>=8.0.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cloud-browser-use-mcp-server=cloud_browser_use_mcp_server.server:main",
        ],
    },
    author="Hadi Hazarabad",
    author_email="mhazarabad@gmail.com",
    description="An unofficial Model Context Protocol server for automating browser tasks using Browser Use API. This package is not provided or endorsed by Browser Use.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mhazarabad/browser-use-mcp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
) 