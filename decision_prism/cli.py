"""CLI 入口点（基于 Typer）。"""

import json

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from decision_prism.config import get_settings
from decision_prism.main import run_debate

app = typer.Typer(
    name="decision-prism",
    help="Decision Prism Pro — Dynamic Strategic Decision System",
    add_completion=False,
)
console = Console()


@app.command()
def debate(
    query: str = typer.Argument(..., help="The strategic question or scenario to analyze"),
    model: str = typer.Option(None, "--model", "-m", help="Override the LLM model"),
):
    """Run a full 3-round expert debate on the given query."""
    if model:
        settings = get_settings()
        settings.llm_model = model

    with console.status("[bold green]Launching debate...", spinner="dots"):
        try:
            result = run_debate(query)
        except Exception as e:
            console.print(f"[red]Debate failed: {e}[/red]")
            raise typer.Exit(1)

    # 显示结果
    errors = result.get("errors", [])
    if errors:
        console.print(
            Panel(
                "\n".join(f"• {e}" for e in errors),
                title="Errors",
                border_style="yellow",
            )
        )

    experts = result.get("selected_experts", [])
    if experts:
        table = Table(title="Expert Panel", show_lines=True)
        table.add_column("Expert", style="cyan")
        table.add_column("Domain", style="green")
        table.add_column("Stance", style="yellow")
        for expert in experts:
            table.add_row(expert["name"], expert["domain"], expert["stance"])
        console.print(table)

    # 第一轮观点摘要
    r1 = result.get("round_1_statements", [])
    if r1:
        for statement in r1:
            console.print(
                Panel(
                    statement["content"][:500] + ("..." if len(statement["content"]) > 500 else ""),
                    title=f"R1: {statement['expert']} ({statement['stance']})",
                    border_style="blue",
                )
            )

    # 报告
    report = result.get("report", {})
    if report:
        console.print(
            Panel(
                json.dumps(report, indent=2, ensure_ascii=False),
                title="Decision Report",
                border_style="green",
            )
        )

    console.print("[bold green]\nDebate complete![/bold green]")


@app.command()
def info():
    """Show current configuration."""
    settings = get_settings()
    console.print(
        Panel(
            f"Model: {settings.llm_model}\n"
            f"Base URL: {settings.llm_base_url}\n"
            f"Temperature: {settings.llm_temperature}\n"
            f"Max Tokens: {settings.llm_max_tokens}\n"
            f"Max Rounds: {settings.debate_max_rounds}\n"
            f"Expert Count: {settings.debate_expert_count}\n"
            f"MC Simulations: {settings.mc_simulations}\n"
            f"MC Seed: {settings.mc_seed}",
            title="Decision Prism Configuration",
            border_style="cyan",
        )
    )


if __name__ == "__main__":
    app()
