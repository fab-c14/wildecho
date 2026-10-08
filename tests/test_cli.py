"""
Unit tests for WildEcho Typer CLI
"""

from typer.testing import CliRunner

from wildecho.cli import app

runner = CliRunner()


def test_cli_version():
    """Asserts version command outputs Google Gemma 2 and bioacoustics details."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "WildEcho" in result.stdout
    assert "Gemma 2" in result.stdout


def test_cli_catalog_listing():
    """Asserts catalog command displays species table."""
    result = runner.invoke(app, ["catalog"])
    assert result.exit_code == 0
    assert "wood_thrush" in result.stdout
    assert "belted_kingfisher" in result.stdout


def test_cli_catalog_inspect():
    """Asserts catalog inspect displays species identification card."""
    result = runner.invoke(app, ["catalog", "--inspect", "wood_thrush"])
    assert result.exit_code == 0
    assert "Hylocichla mustelina" in result.stdout
    assert "Chanterelle" in result.stdout


def test_cli_listen_session():
    """Asserts listen command completes simulated expedition session."""
    result = runner.invoke(app, ["listen", "--windows", "2", "--delay", "0.0"])
    assert result.exit_code == 0
    assert "Trail Waypoint #01" in result.stdout
    assert "EXPEDITION COMPLETE" in result.stdout
    assert "NDSI" in result.stdout
