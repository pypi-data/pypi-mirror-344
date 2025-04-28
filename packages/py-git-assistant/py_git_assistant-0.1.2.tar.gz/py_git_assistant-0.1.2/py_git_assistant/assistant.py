from py_git_assistant.services.git_service import GitService
from py_git_assistant.services.ui_service import UIService
from py_git_assistant.utils.helpers import safe_ask

def main():
  UIService.show_banner()

  while True:
    option = safe_ask(UIService.ask_main_menu())

    match option:
      case "init":
        GitService.init_repo()
      case "push-all":
        GitService.push_all()
      case "clone":
        GitService.clone_repo()
      case "remote":
        GitService.add_remote_repo()
      case "branch":
        GitService.branch_menu()
      case "exit":
        UIService.exit_assistant()

if __name__ == "__main__":
    main()
