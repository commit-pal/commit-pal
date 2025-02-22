from cmpal.models.config import CommitStyleConfigs
from cmpal.scripts.config import load_config, save_config
from cmpal.scripts.onboard import main as onboard


def main():
    if saved_config := load_config():
        configs: CommitStyleConfigs = CommitStyleConfigs.model_validate(saved_config)
        print(f"Config loaded successfully!\n\n{configs.pretty_print()}")
    else:
        configs: CommitStyleConfigs = onboard()
        save_config(configs.model_dump())
        print(f"Config saved successfully!\n\n{configs.pretty_print()}")


if __name__ == "__main__":
    main()
