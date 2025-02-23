import os
from typing import Optional, TypeVar

from colorama import Fore, Style
from simple_term_menu import TerminalMenu

T = TypeVar("T")


def _clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_error_message(error_message: str):
    print(f"{Fore.RED}Error: {error_message}{Style.RESET_ALL}")


def print_available_commands():
    print(f"{Fore.GREEN}Available commands:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}------------------------------------{Style.RESET_ALL}")
    print("- cmpal --setup: Set up the project with the required configurations")
    print(f"{Fore.CYAN}------------------------------------{Style.RESET_ALL}")


def create_selector(
    options: list[tuple[str, T]],
    prompt: Optional[str],
    default_index: int = 0,
    clear_screen: bool = True,
) -> T:
    _clear_screen() if clear_screen else None
    print(prompt) if prompt else None

    menu = TerminalMenu(
        [opt[0] for opt in options],
        cursor_index=default_index,
        menu_cursor_style=("fg_purple", "bold"),
        menu_highlight_style=("bg_purple", "fg_black"),
        title=None,
        clear_menu_on_exit=True,
    )
    selected_index = menu.show()
    return options[selected_index][1]
