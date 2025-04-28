from py_git_assistant.utils.helpers import safe_ask
from py_git_assistant.services.ui_service import UIService
import subprocess

class GitService:

    @staticmethod
    def init_repo():
        UIService.info("Initializing repository...")
        run(["git", "init"])
        run(["git", "branch", "-M", "main"])
        run(["git", "branch"])

    @staticmethod
    def push_all():
        run(["git", "pull", "origin", "main"])
        run(["git", "status"])
        confirm = safe_ask(UIService.ask_confirm("Commit and push all?"))
        if confirm:
            run(["git", "add", "."])
            run(["git", "status"])
            message = UIService.ask_commit_message()
            run(["git", "commit", "-m", message])
            run(["git", "push", "origin", "main"])

    @staticmethod
    def clone_repo():
        url = safe_ask(UIService.ask_text("Repository URL to clone:"))
        run(["git", "clone", url])

    @staticmethod
    def add_remote_repo():
        url = safe_ask(UIService.ask_text("Repository URL:"))
        run(["git", "remote", "add", "origin", url])

    @staticmethod
    def branch_menu():
        action = safe_ask(UIService.ask_branch_action())
        match action:
            case "create":
                name = safe_ask(UIService.ask_text("New branch name:"))
                run(["git", "checkout", "-b", name])
            case "list":
                run(["git", "branch"])
            case "switch":
                name = safe_ask(UIService.ask_text("Branch name to switch to:"))
                run(["git", "checkout", name])

def run(cmd):
    """Run a subprocess command safely."""
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        UIService.error(f"[ERROR] Command '{' '.join(cmd)}' failed with code {e.returncode}")
        UIService.exit_assistant()
