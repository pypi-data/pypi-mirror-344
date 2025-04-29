import os
import sys
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.panel import Panel
from rich.text import Text
from .explainer import explain_log
from .utils import load_log_file
from rich import box

console = Console()

@click.command()
@click.argument('logfile', required=False)
@click.option('--no-mask', is_flag=True, help="Disable masking sensitive data in logs.")
@click.option('--force', is_flag=True, help="Skip safety warning and send logs directly.")
def cli(logfile, no_mask, force):
    """Explain any error log in colorful English."""
    print_banner()

    console.print(Panel.fit("[bold bright_green]📜 Reading log...[/bold bright_green]", box=box.DOUBLE))

    piped_input = not sys.stdin.isatty()

    if piped_input and not logfile:
        log_content = sys.stdin.read()
    elif logfile:
        log_content = load_log_file(logfile)
    else:
        console.print(Panel.fit("[bold bright_red]❌ No log input provided.[/bold bright_red]", box=box.ROUNDED))
        return

    if not log_content.strip():
        console.print(Panel.fit("[bold bright_red]❌ Log content is empty![/bold bright_red]", box=box.ROUNDED))
        return

    if not force:
        if piped_input:
            warning_message = """
⚠️ [bold bright_yellow]Cannot ask for confirmation because input is piped (stdin used).[/bold bright_yellow]

When you use a pipe (`|`), your input is already coming from another command, and standard input (stdin) is consumed.
This disables the ability to ask for interactive confirmation (y/n) safely.

❗ For your protection, Explain-Log requires explicit consent before sending logs to OpenAI servers.

👉 Please rerun with [bold bright_cyan]--force[/bold bright_cyan] if you are sure you want to continue.
"""
            console.print(Panel.fit(Text.from_markup(warning_message), title="Security Notice", border_style="bright_yellow", box=box.HEAVY))
            return
        else:
            warning_text = """
[bold bright_yellow]⚠️ WARNING:[/bold bright_yellow] You are about to send log data to OpenAI servers.
Sensitive data (secrets, IPs, emails) might be included.
"""
            console.print(Panel.fit(Text.from_markup(warning_text), title="Security Notice", title_align="left", border_style="bright_yellow", box=box.HEAVY))
            confirm = console.input("\n[bold bright_yellow]❓ Do you want to continue? (y/n): [/bold bright_yellow]").strip().lower()
            if confirm not in ('y', 'yes'):
                abort_message = """
❌ [bold bright_red]Operation Aborted.[/bold bright_red]

This tool sends your logs to OpenAI for analysis.
Since you did not explicitly confirm consent (y/yes), 
we have safely canceled the operation to protect your data privacy.

👉 Please rerun and confirm if you wish to proceed.
"""
                console.print(
                    Panel.fit(Text.from_markup(abort_message), title="Consent Required", border_style="bright_red", box=box.ROUNDED))
                return

    console.print(Panel.fit("[bold bright_blue]🧠 Analyzing your log with AI...[/bold bright_blue]", box=box.DOUBLE_EDGE))

    with console.status("[bold bright_green]Thinking... analyzing root cause[/bold bright_green]", spinner="earth"):
        explanation = explain_log(log_content, no_mask=no_mask)

    console.print(Panel.fit("[bold bright_green]✅ Analysis Result:[/bold bright_green]\n", box=box.DOUBLE))
    console.print(Markdown(explanation))
    console.print("\n💡 [bold bright_magenta]Tip:[/bold bright_magenta] Always double-check before sharing externally.\n")

def print_banner():
    banner = Text("""
███████╗██╗  ██╗██████╗ ██╗      █████╗ ██╗███╗   ██╗
██╔════╝██║  ██║██╔══██╗██║     ██╔══██╗██║████╗  ██║
███████╗███████║██████╔╝██║     ███████║██║██╔██╗ ██║
╚════██║██╔══██║██╔═══╝ ██║     ██╔══██║██║██║╚██╗██║
███████║██║  ██║██║     ███████╗██║  ██║██║██║ ╚████║
╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
    """, style="bold bright_cyan")
    console.print(banner)
    console.print("[bold bright_magenta]Explain-Log 🔥 — Understand your logs like a PRO.[/bold bright_magenta]\n")
