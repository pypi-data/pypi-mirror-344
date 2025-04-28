![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

# 📜 Git Assistant

🎯 A simple command-line assistant (CLI) to make common Git operations like **initializing repositories**, **committing changes**, **pushing**, **managing branches**, and more — fast and interactive!

---

## ✨ Features

- Initialize local and remote Git repositories.
- Quickly `git add`, `commit`, and `push` in one flow.
- Create, list, and switch between branches easily.
- Clone remote repositories.
- Guided commit types and messages.
- Colored terminal output for better visibility.
- Fully interactive and beginner-friendly!

---

## 🚀 Installation

> Recommended: Use a virtual environment (`venv`)

1. Clone the repository:

2. Install the project:

```bash
pip install .
```

3. Now you can use the assistant globally:

```bash
git-assistant
```

---

## 🛠️ Usage

After installation, simply run:

```bash
git-assistant
```

You will see an interactive menu like:

```text
What fo you want to do?
> Init repo       (Initialize Git and remote)
> Push all        (Add, commit, and push changes)
> Clone repo      (Clone a remote repository)
> Manage branch   (Create/Switch branches)
> Exit
```

![git assistant CLI](assets/py-git-assistant-CLI.png)

Follow the prompts and let the assistant guide your Git workflow!

---

## 📂 Project Structure

```bash
git_assistant/
│
├── git_assistant/
│   ├── __init__.py
│   ├── assistant.py        # Main entry file
│   ├── services/
│   │   ├── __init__.py
│   │   ├── git_service.py  # Git-related commands
│   │   └── ui_service.py   # User interaction and menus
│   └── utils/
│       ├── __init__.py
│       └── helpers.py      # Helper functions
│
├── requirements.txt        # Project dependencies
├── .gitignore
├── README.md               # Project documentation
├── pyproject.toml          # For packaging and distribution

```
