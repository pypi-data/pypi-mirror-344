from setuptools import setup, find_packages

setup(
    name="explain-log",
    version="0.1.0",
    packages=find_packages(),   # <-- find_packages will find "explain_log" automatically
    install_requires=[
        "openai",
        "click",
        "rich",
        "python-dotenv",
    ],
    entry_points={
        'console_scripts': [
            'explain-log=explain_log.main:cli',   # <-- updated path
        ],
    },
    author="Your Name",
    description="CLI tool to explain logs using OpenAI",
    keywords="cli devops logs openai explanation",
    python_requires='>=3.8',
)
