import os
import re
from openai import OpenAI
from rich.console import Console

console = Console()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_TOKENS_ESTIMATE = 6000  # reasonable safe limit (input only)
APPROX_CHARS_PER_TOKEN = 4  # OpenAI says ~4 chars per token

def sanitize_log(log_content: str) -> str:
    # Simple sanitization
    log_content = re.sub(r'\b[\w.-]+?@\w+?\.\w+?\b', '[EMAIL REDACTED]', log_content)
    log_content = re.sub(r'\b\d{1,3}(?:\.\d{1,3}){3}\b', '[IP REDACTED]', log_content)
    log_content = re.sub(r'(http|https)://[^\s]+', '[URL REDACTED]', log_content)
    return log_content

def truncate_log(log_content: str) -> str:
    max_chars = MAX_TOKENS_ESTIMATE * APPROX_CHARS_PER_TOKEN
    if len(log_content) > max_chars:
        console.print(
            "[bold yellow]⚠️ Log was very large. Analyzing summarized version (start and end only).[/bold yellow]")
        head = log_content[:max_chars // 2]
        tail = log_content[-(max_chars // 2):]
        return f"=== Start of Log ===\n{head}\n=== Skipping Middle (truncated) ===\n{tail}"
    else:
        return log_content

def explain_log(log_content: str, no_mask: bool = False) -> str:
    if not no_mask:
        log_content = sanitize_log(log_content)

    log_content = truncate_log(log_content)

    prompt = f"""
You are a DevOps Senior Engineer.
The user will send you a log file output.

Your job:
- Explain in clear English what went wrong.
- Highlight the main problem.
- Suggest possible fixes or troubleshooting steps.
- Be professional, clear, and concise.

Here is the log:

{log_content}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a senior DevOps engineer specializing in log troubleshooting."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=600,
    )

    return response.choices[0].message.content.strip()
