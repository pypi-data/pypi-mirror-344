from click.testing import CliRunner
# from unittest.mock import patch

from gha_deploy.cli import deploy

def test_deploy_cli():
    """Unit test for running the CLI"""
    runner = CliRunner()
    result = runner.invoke(deploy, ["GHA-Deploy-CLI", "Unit-Test.yml", "main"])

    assert result.exit_code == 0
    assert "GitHub Action triggered successfully!" in result.output
    assert "Waiting for Job to finish..." in result.output
    assert "Workflow completed successfully! ✅" in result.output

def test_deploy_cli_no_track():
    """Unit test for running the CLI with --no-track flag"""
    runner = CliRunner()
    result = runner.invoke(deploy, ["GHA-Deploy-CLI", "Unit-Test.yml", "main", "--no-track"])

    assert result.exit_code == 0
    assert "GitHub Action triggered successfully!" in result.output

def test_deploy_cli_inputs():
    """Unit test for running the CLI with --inputs"""
    runner = CliRunner()
    result = runner.invoke(deploy, ["GHA-Deploy-CLI", "Unit-Test.yml", "main", "--inputs", '{"test1": "test", "test2": "testagain"}'])

    assert result.exit_code == 0
    assert "GitHub Action triggered successfully!" in result.output
    assert "Waiting for Job to finish..." in result.output
    assert "Workflow completed successfully! ✅" in result.output
    