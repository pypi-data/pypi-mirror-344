import questionary
from colorama import Fore
import textwrap

class UIService:

  @staticmethod
  def show_banner():
    print(textwrap.dedent(f'''
        {Fore.GREEN}==========================================
                  Git Assistant Started        
        ==========================================
    '''))

  @staticmethod
  def ask_main_menu():
    return questionary.select(
      "What do you want to do?",
      choices=[
        questionary.Choice(title="Init repo", value="init"),
        questionary.Choice(title="Push all changes", value="push-all"),
        questionary.Choice(title="Clone repository", value="clone"),
        questionary.Choice(title="Branch management", value="branch"),
        questionary.Choice(title="Exit", value="exit"),
      ]
    )

  @staticmethod
  def ask_commit_message():
    type_ = questionary.select(
      "Choose commit type:",
      choices=[
          questionary.Choice(title="docs", value="docs", description="Documentation changes (e.g. README)"),
          questionary.Choice(title="chore", value="chore", description="Configuration or maintenance tasks (e.g. .env updates)"),
          questionary.Choice(title="feat", value="feat", description="New feature"),
          questionary.Choice(title="fix", value="fix", description="Bug fixes"),
          questionary.Choice(title="refactor", value="refactor", description="Code refactoring (no functionality change)"),
          questionary.Choice(title="test", value="test", description="Adding or fixing tests"),
          questionary.Choice(title="style", value="style", description="Style changes (e.g. formatting, missing semicolons)"),
          questionary.Choice(title="perf", value=":perf", description="Performance improvements"),
          questionary.Choice(title="ci", value="ci", description="Continuous Integration changes"),
          questionary.Choice(title="build", value="build", description="Changes that affect the build process"),
          questionary.Choice(title="revert", value="revert", description="Reverts a previous commit"),
          questionary.Choice(title="other", value="other", description="Write your message")
        ]
      ).ask()

    message = questionary.text("Commit message:").ask()
    return f"{type_}: {message}" if type_ != "other" else message

  @staticmethod
  def ask_confirm(message):
      return questionary.confirm(message)

  @staticmethod
  def ask_text(message):
      return questionary.text(message)

  @staticmethod
  def ask_branch_action():
      return questionary.select(
          "Branch action:",
          choices=[
              questionary.Choice(title="Create new branch", value="create"),
              questionary.Choice(title="List branches", value="list"),
              questionary.Choice(title="Switch branch", value="switch"),
          ]
      )

  @staticmethod
  def info(message):
      print(f"{Fore.BLUE}[INFO]{Fore.RESET} {message}")

  @staticmethod
  def error(message):
      print(f"{Fore.RED}[ERROR]{Fore.RESET} {message}")

  @staticmethod
  def exit_assistant():
      print(f"{Fore.RED}Goodbye!")
      exit(0)
