from cmpal.scripts.config import load_config, save_config
from cmpal.scripts.onboard import main as onboard


def main():
    # FOR TESTING
    onboard()

    if not (config := load_config()):
        onboard()
        save_config({"test": "test"})
        config = load_config()


if __name__ == "__main__":
    main()
