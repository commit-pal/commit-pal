import sys

from cmpal.models.config import CommitStyleConfigs
from cmpal.scripts.config import load_config, save_config
from cmpal.scripts.onboard import main as onboard
from cmpal.utils.format import print_available_commands, print_error_message


def main():
    if len(sys.argv) > 2:
        print_error_message("Too many arguments provided.")
        return 1
    elif len(sys.argv) == 1:
        # TODO: Invoke inference if config is found, else invoke setup
        return 0

    match sys.argv[1]:
        case "--setup" | "--init":
            return setup()
        case "--help":
            print_available_commands()
            return 0
        case _:
            print_error_message("Invalid argument provided.")
            print_available_commands()
            return 1


def setup():
    try:
        if saved_config := load_config():
            configs: CommitStyleConfigs = CommitStyleConfigs.model_validate(saved_config)
            print(f"Config loaded successfully!\n\n{configs.pretty_print()}")
        else:
            configs: CommitStyleConfigs = onboard()
            save_config(configs.model_dump())
            print(f"Config saved successfully!\n\n{configs.pretty_print()}")
        return 0
    except KeyboardInterrupt:
        print("\nSetup cancelled. You can run setup again using 'cmpal-setup'")
        return 1
