"""
This File is the entrypoint for the tool. It defines the inputs and calls the github_api functions
"""

import click
from .github_api import trigger_workflow

# Mandatory inputs
@click.command()
@click.argument("repo", required=False)
@click.argument("workflow", required=False)
@click.argument("ref", required=False)
@click.option("--repo", "repo_opt", help="The repository to deploy.")
@click.option("--workflow", "workflow_opt", help="The workflow file to trigger.")
@click.option("--ref", "ref_opt", help="The Git ref (e.g., branch or tag) for the deployment.")

#optional inputs/flags
@click.option("--no-track", is_flag=True, help="Don't poll the workflow after triggering it.")
@click.option("--inputs", "inputs", required=False, help="Optional: JSON object containing action input parameters.")



def deploy(repo, workflow, ref, repo_opt, workflow_opt, ref_opt, no_track, inputs):
    # Use flags if provided, otherwise fallback to positional args
    final_repo = repo_opt or repo
    final_workflow = workflow_opt or workflow
    final_ref = ref_opt or ref

    if not final_repo or not final_workflow or not final_ref:
        raise click.UsageError("You must provide repo, workflow, and ref")

    trigger_workflow(final_repo, final_workflow, final_ref, no_track, inputs)
