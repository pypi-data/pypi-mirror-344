"""
Run commands.
Grab keys from environment.

Submission:
- Get things out of VCS.
- Convert to actions.
- Send to Lando Headless.

Job status:
- Request job status
- Request repo mappings (see bhearsum chat)

Commands:
    - push commits
    - push tag
    - push merge
"""

import os
import pprint
import subprocess
import time
import tomllib
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Optional

import click
import requests

DEFAULT_CONFIG_PATH = Path.home() / ".mozbuild" / "lando.toml"


@dataclass
class Config:
    """Configuration options for the Lando CLI.

    Default location for the config is `~/.mozbuild/lando.toml`.
    """

    api_token: str
    lando_url: str
    user_email: str

    @classmethod
    def load_config(cls) -> "Config":
        """Load config from the filesystem."""
        config_path = Path(os.getenv("LANDO_CONFIG_PATH", DEFAULT_CONFIG_PATH))
        config_data = {}

        if config_path.is_file():
            with config_path.open("rb") as f:
                config_data = tomllib.load(f)

        api_token = os.getenv("LANDO_HEADLESS_API_TOKEN") or config_data["api_token"]
        user_email = os.getenv("LANDO_USER_EMAIL") or config_data["user_email"]
        lando_url = os.getenv(
            "LANDO_URL", config_data.get("lando_url", "https://lando.moz.tools")
        )

        return Config(api_token=api_token, user_email=user_email, lando_url=lando_url)


def with_config(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        config = Config.load_config()
        return func(config, *args, **kwargs)

    return wrapper


def api_request(
    config: Config,
    method: str,
    path: str,
    *args,
    headers: Optional[dict] = None,
    **kwargs,
) -> requests.Response:
    """Send an HTTP request to the Lando Headless API.

    `config` is the loaded `Config` for the CLI.
    `method` is the HTTP method to use, ie `GET`, `POST`, etc.
    `path` is the REST API endpoint to send the request to.
    `headers` is the set of HTTP headers to pass to the request.

    All other arguments in *args and **kwargs are passed through to `requests.request`.
    """
    url = f"{config.lando_url}/api/{path}"

    common_headers = {
        "Authorization": f"Bearer {config.api_token}",
        "User-Agent": f"Lando-User/{config.user_email}",
    }
    if headers:
        common_headers.update(headers)

    return requests.request(method, url, *args, headers=common_headers, **kwargs)


def get_job_status(config: Config, job_id: int) -> dict:
    """Return the status of the job."""
    result = api_request(config, "GET", f"job/{job_id}")

    # `200` is a successful return.
    if result.status_code != 200:
        result.raise_for_status()

    return result.json()


def post_actions(config: Config, repo_name: str, actions: list[dict]) -> dict:
    """Send actions to the headless API."""
    actions_json = {"actions": actions}
    result = api_request(config, "POST", f"repo/{repo_name}", json=actions_json)

    # `202` is a successful return.
    if result.status_code != 202:
        print("Encountered an error submitting job to Lando:")

        try:
            response_json = result.json()
            print(response_json["details"])
        except Exception:
            print("Unknown error.")

        result.raise_for_status()

    return result.json()


def wait_for_job_completion(
    config: Config, job_id: int, poll_interval: int = 3
) -> dict:
    """Wait for a job to complete."""
    print("Waiting for job completion, you may exit at any time.")
    print(f"Note: run `lando check-job {job_id}` to check the status later.")

    while True:
        result = get_job_status(config, job_id)

        status = result["status"]

        if status == "SUBMITTED":
            print("Job has been submitted and will be started soon.")
        elif status == "IN_PROGRESS":
            print("Job is in progress.")
        elif status == "FAILED":
            error_details = result.get("details", "No additional details provided.")
            print(f"Job {job_id} failed: {error_details}")
            break

        elif status == "LANDED":
            print(f"Job {job_id} landed successfully.")
            break

        elif status == "CANCELLED":
            print(f"Job {job_id} has been cancelled.")
            break

        else:
            print(f"Job {job_id} had unexpected status: `{status}`.")
            break

        time.sleep(poll_interval)

    return result


def submit_to_lando(config: Config, repo_name: str, actions: list[dict]):
    print("Sending actions:")
    pprint.pprint(actions)

    response = post_actions(config, repo_name, actions)

    job_id = response["job_id"]
    print(f"Job {job_id} successfully submitted to Lando")

    wait_for_job_completion(config, job_id)
    return


def git_run(git_args: list[str], repo: Path) -> str:
    command = ["git", *git_args]
    result = subprocess.run(
        command,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
        cwd=repo,
    )
    return result.stdout.strip()


def get_remote_branch(branch: str) -> str:
    # TODO more complicated branch getting
    return f"origin/{branch}"


def get_new_commits(local_branch: str, repo: Path) -> list[str]:
    remote_branch = get_remote_branch(local_branch)
    print(f"Using remote branch {remote_branch}")

    commits = git_run(
        ["rev-list", f"{remote_branch}..{local_branch}", "--reverse"], repo
    ).splitlines()

    print(f"found {len(commits)} new commits")
    return commits


def get_commit_patches(commits: list[str], repo: Path) -> list[str]:
    patches = []
    for idx, commit in enumerate(commits):
        print(f"Getting patch for commit {idx}")
        patch = git_run(["format-patch", commit, "-1", "--always", "--stdout"], repo)
        patches.append(patch)

    return patches


def get_commit_message(commit_hash: str, repo: Path) -> str:
    return git_run(["log", "-1", "--pretty=%B", commit_hash], repo)


def detect_new_tags(repo: Path) -> set[str]:
    print("Detecting new tags")

    local_tags_set = set(git_run(["tag", "--list"], repo).splitlines())
    remote_tags = git_run(["ls-remote", "--tags", "origin"], repo).splitlines()
    remote_tags_set = {
        line.split("refs/tags/")[1] for line in remote_tags if "refs/tags/" in line
    }

    return local_tags_set - remote_tags_set


def create_tag_actions(local_only_tags: set[str], repo: Path) -> list[dict]:
    tags_to_push = []
    for tag in local_only_tags:
        commit = git_run(["rev-list", "-n", "1", tag], repo)
        tags_to_push.append({"name": tag, "commit": commit})

    return tags_to_push


def detect_merges(commits: list[str], repo: Path) -> list[dict[str, str]]:
    # TODO detecting already existent merge
    print("Detecting merge")

    merges = []
    for commit in commits:
        parents = git_run(["rev-list", "--parents", "-n", "1", commit], repo).split()
        if len(parents) > 2:
            commit_message = get_commit_message(commit, repo)
            target_commit = parents[2]  # Merged commit (the one merged onto)
            merges.append(
                {
                    "source_commit": commit,
                    "target": target_commit,
                    "commit_message": commit_message,
                }
            )
    return merges


def get_current_branch(repo: Path) -> str:
    return git_run(["branch", "--show-current"], repo)


@click.group()
def cli():
    """Lando headless CLI."""


@cli.command()
@click.option(
    "--local-repo",
    help="Local repo to work with.",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path),
    default=Path("/home/sheehan/conduit/ff-test"),
)
@click.option("--lando-repo", help="Lando repo to post changes to.")
@with_config
def push_commits(config: Config, local_repo: Path, lando_repo: str):
    """Push new commits to the specified repository."""
    print(f"Repo path is {local_repo}")

    current_branch = get_current_branch(local_repo)
    print(f"Using branch {current_branch}")

    commits = get_new_commits(current_branch, local_repo)
    if not commits:
        print("No new commits found!")
        return 1

    patches = get_commit_patches(commits, local_repo)
    actions = [
        {"action": "add-commit", "content": patch, "patch_format": "git-format-patch"}
        for patch in patches
    ]

    return submit_to_lando(config, lando_repo, actions)


@cli.command()
@click.option(
    "--local-repo",
    help="Local repo to work with.",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path),
    default=Path("/home/sheehan/conduit/ff-test"),
)
@click.option("--lando-repo", help="Lando repo to post changes to.")
@with_config
def push_tag(config: Config, local_repo: Path, lando_repo: str):
    """Push new tags to the specified repository."""
    print(f"Repo path is {local_repo}")

    new_tags = detect_new_tags(local_repo)
    if not new_tags:
        print("No new tags found.")
        return

    tag_actions = create_tag_actions(new_tags, local_repo)
    actions = [
        {"action": "tag", "name": tag["name"], "target": tag["commit"]}
        for tag in tag_actions
    ]

    return submit_to_lando(config, lando_repo, actions)


@cli.command()
@click.option(
    "--local-repo",
    help="Local repo to work with.",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path),
    default=Path("/home/sheehan/conduit/ff-test"),
)
@click.option("--lando-repo", help="Lando repo to post changes to.")
@with_config
def push_merge(config: Config, local_repo: Path, lando_repo: str):
    """Push merge actions to the specificed repository."""
    print(f"Repo path is {local_repo}")

    current_branch = get_current_branch(local_repo)
    print(f"Using branch {current_branch}")

    new_commits = get_new_commits(current_branch, local_repo)
    actions = detect_merges(new_commits, local_repo)
    if not actions:
        print("No new merge commits found.")
        return 1

    return submit_to_lando(config, lando_repo, actions)


@cli.command("check-job")
@click.argument("job_id", type=int)
@with_config
def check_job(config: Config, job_id: int):
    """Check the status of a previously submitted job."""
    wait_for_job_completion(config, job_id)
