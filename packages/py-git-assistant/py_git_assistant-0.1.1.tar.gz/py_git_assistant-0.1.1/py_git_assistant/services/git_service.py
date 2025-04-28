from py_git_assistant.utils.helpers import safe_ask
from py_git_assistant.services.ui_service import UIService
import subprocess

class GitService:

    @staticmethod
    def init_repo():
        UIService.info("Initializing repository...")
        run("git init")
        run("git branch -M main")
        run ("git branch")

    @staticmethod
    def push_all():
        run("git pull origin main")
        run("git status")
        confirm = safe_ask(UIService.ask_confirm("Commit and push all?"))
        if confirm:
            run("git add .")
            run("git status")
            message = UIService.ask_commit_message()
            run(f'git commit -m "{message}"')
            run("git push origin main")

    @staticmethod
    def clone_repo():
        url = safe_ask(UIService.ask_text("Repository URL to clone:"))
        run(f"git clone {url}")

    @staticmethod
    def branch_menu():
        action = safe_ask(UIService.ask_branch_action())
        match action:
            case "create":
                name = safe_ask(UIService.ask_text("New branch name:"))
                run(f"git checkout -b {name}")
            case "list":
                run("git branch")
            case "switch":
                name = safe_ask(UIService.ask_text("Branch name to switch to:"))
                run(f"git checkout {name}")

def run(cmd):
    try:
        subprocess.run(cmd.split(), check=True)
    except subprocess.CalledProcessError as e:
        UIService.error(f"Failed: {e}")
        UIService.exit_assistant()
