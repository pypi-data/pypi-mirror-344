from py_git_assistant.services.ui_service import UIService

def safe_ask(prompt):
    value = prompt.ask()
    if value is None:
        UIService.exit_assistant()
    return value

