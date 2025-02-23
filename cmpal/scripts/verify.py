from cmpal.utils.terminal import create_selector


def verify_commit_message() -> bool:
    return create_selector(
        options=[
            ("Accept", True),
            ("Reject", False),
        ],
        prompt=None,
        clear_screen=False,
    )
