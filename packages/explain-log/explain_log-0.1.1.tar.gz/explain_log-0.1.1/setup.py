from setuptools import setup, find_packages

# Read README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="explain-log",
    version="0.1.1",
    author="Tasrie IT Services",
    author_email="info@tasrieit.com",
    description="Explain your DevOps logs instantly using OpenAI with a colorful CLI.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # important!
    url="https://github.com/yourgithub/explain-log",
    project_urls={
        "Bug Tracker": "https://github.com/tasrieitservices/explain-log/issues",
    },
    packages=find_packages(),
    install_requires=[
        "openai",
        "click",
        "rich",
        "python-dotenv",
    ],
    entry_points={
        'console_scripts': [
            'explain-log=explain_log.main:cli',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
