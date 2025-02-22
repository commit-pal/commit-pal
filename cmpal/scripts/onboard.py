from typing import TypeVar

from simple_term_menu import TerminalMenu

from cmpal.models.config import CapitalizationStyle

T = TypeVar("T")


def _format_question(question: str) -> str:
    return f"\033[1;32m{question}\033[0m"


def create_selector(options: list[tuple[str, T]], prompt: str, default_index: int = 0) -> T:
    menu = TerminalMenu(
        [opt[0] for opt in options],
        title=prompt,
        cursor_index=default_index,
        menu_cursor_style=("fg_purple", "bold"),
        menu_highlight_style=("bg_purple", "fg_black"),
    )
    selected_index = menu.show()
    return options[selected_index][1]


def main():
    print("Welcome to commit-pal! Let's get started~\n")
    capitalization_style = create_selector(
        options=[
            ("lowercase (default)", CapitalizationStyle.LOWERCASE),
            ("capitalized", CapitalizationStyle.CAPITALIZED),
        ],
        prompt=f"""{_format_question("Should the subject line start with a capital letter?")}

Examples:
- lowercase: \"add support for git hooks\"
- capitalized: \"Add support for git hooks\"
""",
    )
