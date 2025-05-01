"""
This file contains all of the functions that will interact with the github API
"""

import os
import time
import json
import requests
import click


def trigger_workflow(repo, workflow, ref, no_track, inputs=""):
    # CLI workflow
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise click.UsageError("Error: GITHUB_TOKEN environment variable is required.")
    
    parsed_inputs = {}
    if inputs:
        parsed_inputs = json.loads(inputs)

    run_action(github_token, repo, workflow, ref, parsed_inputs)
    time.sleep(3)
    if not no_track:
        poll_action(github_token, "ktierney15", repo)




def run_action(token: str, repo: str, workflow: str, ref: str = "main", inputs: dict = {}):
    repo_owner = "ktierney15"
    workflow_id = get_workflow_id(token, repo_owner, repo, workflow)

    url = f"https://api.github.com/repos/{repo_owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        "ref": ref
    }

    if inputs:
        data["inputs"] = inputs

    response = requests.post(url, json=data, headers=headers, timeout=10)
    if response.status_code == 204:
        print("GitHub Action triggered successfully!")
        return
    else:
        raise click.UsageError(f"Failed to trigger GitHub Action: {response.status_code}, {response.text}")


def get_workflow_id(token: str, repo_owner: str, repo: str, workflow_filename: str):
    if not token:
        print("GitHub token not found in environment variables.")
        return None

    url = f"https://api.github.com/repos/{repo_owner}/{repo}/actions/workflows"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        workflows = response.json()['workflows']
        for workflow in workflows:
            if workflow['path'].split("/")[-1] == workflow_filename:
                return workflow['id']
        raise click.UsageError(f"Error: Workflow file {workflow_filename} does not exist in {repo_owner}/{repo}.")
    else:
        raise click.UsageError(f"Error: Failed to fetch workflows {response.status_code}, {response.text}")


def poll_action(token: str, repo_owner: str, repo: str):
    print("Waiting for Job to finish...")
    while True:
        url = f"https://api.github.com/repos/{repo_owner}/{repo}/actions/runs"
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            runs_data = response.json()
            latest_run = runs_data['workflow_runs'][0]
            status = latest_run['status']
            conclusion = latest_run['conclusion']

            if status == 'completed':
                if conclusion == 'success':
                    print("Workflow completed successfully! ✅")
                else:
                    print("Workflow failed. ❌")
                print(f"View the run at: {latest_run['html_url']}")
                break
