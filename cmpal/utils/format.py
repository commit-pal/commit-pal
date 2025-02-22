import re


def format_poetry_lock_diff(content: str) -> str:
    # Find all package blocks with their name and version changes
    package_pattern = r'\[\[package\]\]\s*(?:(?:-|\+)?name.*?\n)(?:-version.*?\n\+version.*?\n|(?:-|\+)?version.*?\n)'
    matches = re.findall(package_pattern, content, re.MULTILINE)
    
    # Add file name to each block and join
    formatted_blocks = []
    for match in matches:
        if match.strip():
            formatted_blocks.append(f"poetry.lock\n{match.strip()}")
    
    return "\n\n".join(formatted_blocks) 
