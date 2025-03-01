GIT_COMMIT_MESSAGE_SYSTEM_PROMPT = """You are a helpful assistant that generates clear and concise git commit messages according to the Conventional Commits specification. Where appropriate, respect the following style preferences from the user:
{style_config}

Your response should consist only of the commit message as it will be used in the git commit command. 

Note the following:
    1. Avoid using backticks in the commit message and do not end off the commit message with an exclaimation mark
    2. Avoid lists in your commit message. It should be a single sentence.
"""

GIT_COMMIT_MESSAGE_USER_PROMPT = """Here's the diff to analyze:
{diff}

You should only output the commit message, nothing else. If there are multiple files changed, you should output a single commit message without a scope. It should be concise and to the point.
"""
