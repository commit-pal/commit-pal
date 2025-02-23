from cmpal.models.config import (
    BreakingChangeIndicator,
    CapitalizationStyle,
    CommitStyleConfigs,
    FooterFormat,
    PunctuationStyle,
    ScopeFormat,
)
from cmpal.scripts.config import save_config
from cmpal.utils.terminal import create_selector


def _format_question(question: str, examples: dict[str, str] | None) -> str:
    examples_str = ""
    if examples:
        examples_str = "Examples:\n" + "\n".join(f'- {k}: "{v}"' for k, v in examples.items())
        return f"""\033[1;32m{question}\033[0m\n\n{examples_str}\n"""
    return f"""\033[1;32m{question}\033[0m\n"""


def _onboard() -> CommitStyleConfigs:
    print("Welcome to commit-pal! Let's sort out some stylistic preferences.")
    capitalization = create_selector(
        options=[
            ("lowercase (default)", CapitalizationStyle.LOWERCASE),
            ("capitalized", CapitalizationStyle.CAPITALIZED),
        ],
        prompt=_format_question(
            question="Should the subject line start with a capital letter?",
            examples={
                "lowercase": "add support for git hooks",
                "capitalized": "Add support for git hooks",
            },
        ),
    )
    punctuation = create_selector(
        options=[
            ("without punctuation (default)", PunctuationStyle.WITHOUT_PERIOD),
            ("with punctuation", PunctuationStyle.WITH_PERIOD),
        ],
        prompt=_format_question(
            question="Should the subject line end with a period?",
            examples={
                "without punctuation": "add support for git hooks",
                "with punctuation": "add support for git hooks.",
            },
        ),
    )
    scope_format = create_selector(
        options=[
            ("parentheses (default)", ScopeFormat.PARENTHESES),
            ("brackets", ScopeFormat.BRACKETS),
            ("none", ScopeFormat.NONE),
        ],
        prompt=_format_question(
            question="Should the scope be formatted?",
            examples={
                "parentheses": "feat(scope): message",
                "brackets": "feat[scope]: message",
                "none": "feat: message",
            },
        ),
    )
    breaking_change_indicator = create_selector(
        options=[
            ("exclamation mark (default)", BreakingChangeIndicator.EXCLAMATION_MARK),
            ("footer only", BreakingChangeIndicator.FOOTER_ONLY),
        ],
        prompt=_format_question(
            question="How should breaking changes be indicated?",
            examples={
                "exclamation mark in header": "feat!: message",
                "footer": "feat: message\n\nBREAKING CHANGE: message",
            },
        ),
    )
    footer_format = create_selector(
        options=[
            ("KEY: VALUE (default)", FooterFormat.KEY_VALUE_COLON),
            ("KEY=VALUE", FooterFormat.KEY_VALUE_EQUALS),
        ],
        prompt=_format_question(
            question="How should footers be formatted?",
            examples={
                "KEY: VALUE": "Closes: #123",
                "KEY=VALUE": "Closes=#123",
            },
        ),
    )
    max_subject_length = create_selector(
        options=[
            ("72 characters (default)", 72),
            ("50 characters", 50),
            ("100 characters", 100),
        ],
        prompt=_format_question(question="Maximum length of the subject line?", examples=None),
    )
    return CommitStyleConfigs(
        capitalization=capitalization,
        punctuation=punctuation,
        scope_format=scope_format,
        breaking_change_indicator=breaking_change_indicator,
        footer_format=footer_format,
        max_subject_length=max_subject_length,
    )


def setup():
    try:
        configs: CommitStyleConfigs = _onboard()
        save_config(configs.model_dump())
        print(f"Config saved successfully!\n\n{configs.pretty_print()}")
        return 0
    except KeyboardInterrupt:
        print("\nSetup cancelled. You can run setup again using 'cmpal-setup'")
        return 1
