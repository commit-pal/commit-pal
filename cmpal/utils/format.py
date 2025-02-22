import re

from colorama import Fore, Style


def format_poetry_lock_diff(content: str) -> str:
    # Find all package blocks with their name and version changes
    package_pattern = r"\[\[package\]\]\s*(?:(?:-|\+)?name.*?\n)(?:-version.*?\n\+version.*?\n|(?:-|\+)?version.*?\n)"
    matches = re.findall(package_pattern, content, re.MULTILINE)

    # Add file name to each block and join
    formatted_blocks = []
    for match in matches:
        if match.strip():
            formatted_blocks.append(f"poetry.lock\n{match.strip()}")

    return "\n\n".join(formatted_blocks)


def print_error_message(error_message: str):
    print(f"{Fore.RED}Error: {error_message}{Style.RESET_ALL}")


def print_available_commands():
    print(f"{Fore.GREEN}Available commands:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}------------------------------------{Style.RESET_ALL}")
    print("- cmpal --setup: Set up the project with the required configurations")
    print(f"{Fore.CYAN}------------------------------------{Style.RESET_ALL}")
