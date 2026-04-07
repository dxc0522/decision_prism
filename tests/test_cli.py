"""CLI tests."""

from typer.testing import CliRunner

from decision_prism.cli import app

runner = CliRunner()


def test_info_command():
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "Decision Prism Configuration" in result.stdout
    assert "Model:" in result.stdout


def test_debate_command_missing_query():
    result = runner.invoke(app, ["debate"])
    assert result.exit_code != 0
