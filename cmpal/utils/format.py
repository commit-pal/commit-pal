import re



def format_poetry_lock_diff(content: str) -> str:
    # Find all package blocks including additions, removals, and changes
    package_pattern = r"(?:^|\n)((?:[-+ ])\[\[package\]\].*?\n(?:[-+ ].*?\n)+)"
    matches = re.findall(package_pattern, content, re.MULTILINE)

    formatted_blocks = []
    file_header_added = False

    for match in matches:
        if not match.strip():
            continue

        # Remove any leading newline and get clean lines
        lines = match.lstrip("\n").split("\n")

        # Extract package info
        package_info = []
        name = version = old_version = None

        # Track if we've seen both additions and deletions
        has_addition = any(line.startswith("+") for line in lines)
        has_deletion = any(line.startswith("-") for line in lines)
        is_update = has_addition and has_deletion

        for line in lines:
            if "name = " in line:
                # Get name from any non-modified line or modified line
                name_val = line.lstrip("+ -").split("=")[1].strip().strip('"')
                if name is None:  # Only set name once
                    name = name_val
            elif line.startswith("+") and "version = " in line:
                version = line.split("=")[1].strip().strip('"')
            elif line.startswith("-") and "version = " in line:
                old_version = line.split("=")[1].strip().strip('"')

        # Format based on change type
        if has_addition and has_deletion and name and version and old_version:
            package_info.append(f"Updated {name} {old_version} → {version}")
        elif has_deletion and name and old_version and not has_addition:
            package_info.append(f"Removed {name} {old_version}")
        elif has_addition and name and version and not has_deletion:
            package_info.append(f"Added {name} {version}")

        if package_info:
            if not file_header_added:
                formatted_blocks.append("poetry.lock")
                file_header_added = True
            formatted_blocks.append("\n".join(package_info))

    return "\n".join(formatted_blocks)


def format_yarn_lock_diff(content: str) -> str:
    # Find all package blocks including additions, removals, and changes
    # Matches package blocks that are either:
    # - Entirely new (all lines prefixed with +)
    # - Entirely removed (all lines prefixed with -)
    # - Modified (mix of +/- lines)
    package_pattern = r'(?:^|\n)((?:\+|\-)?"?@?[^"]+@[^:]+"?:\n(?:[-+ ].*\n)+)'
    matches = re.findall(package_pattern, content, re.MULTILINE)

    # Add file name to each block and join
    formatted_blocks = []
    for match in matches:
        if match.strip():
            # Remove any leading newline that might have been captured
            cleaned_match = match.lstrip("\n")
            formatted_blocks.append(f"yarn.lock\n{cleaned_match.strip()}")

    return "\n\n".join(formatted_blocks)
