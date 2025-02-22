import subprocess
from typing import List, Optional

from cmpal.inference.llm import OllamaEngine
from cmpal.utils.format import format_poetry_lock_diff


def get_staged_files() -> List[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, check=True
        )
        return [f for f in result.stdout.split("\n") if f]
    except subprocess.CalledProcessError:
        return []


def get_changed_files() -> List[str]:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "-uall"], capture_output=True, text=True, check=True
        )
        files = []
        for line in result.stdout.split("\n"):
            if not line:
                continue
            # Status format is "XY PATH" where X and Y are status codes
            status = line[:2]
            path = line[3:].strip()

            # Handle renamed files
            if "=>" in path:
                files.append(path.split("=>")[-1].strip())
            # Handle untracked files and directories
            elif status == "??":
                files.append(path)
            # Handle modified, added, deleted files
            else:
                files.append(path)

        return [f for f in files if f]  # Filter out any empty strings
    except subprocess.CalledProcessError:
        return []


def get_diff(file_path: Optional[str] = None) -> str:
    try:
        cmd = ["git", "diff", "--cached", "--color=never"]
        if file_path:
            cmd.append(file_path)

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if not result.stdout:
            return ""

        # For single file diff
        if file_path:
            return _process_diff_content(file_path, result.stdout)

        # For multiple files diff
        return _process_multiple_diffs(result.stdout)

    except subprocess.CalledProcessError:
        return ""


def _process_diff_content(file_path: str, diff_content: str) -> str:
    """Process diff content based on file type."""
    # Add custom processors for different file types here
    processors = {
        "poetry.lock": format_poetry_lock_diff,
        # Add more file type processors here:
        # "package-lock.json": clean_package_lock_diff,
        # "yarn.lock": clean_yarn_lock_diff,
    }

    file_name = file_path.split("/")[-1]
    processor = processors.get(file_name)
    return processor(diff_content) if processor else diff_content


def _process_multiple_diffs(diff_content: str) -> str:
    """Process multiple file diffs."""
    if not diff_content:
        return ""

    diff_sections = []
    current_file = ""
    current_section = []

    for line in diff_content.split("\n"):
        if line.startswith("diff --git"):
            # Process previous section if exists
            if current_section:
                processed = _process_diff_content(current_file, "\n".join(current_section))
                if processed:
                    diff_sections.append(processed)

            # Start new section
            current_section = [line]
            current_file = line.split()[-1]
        else:
            current_section.append(line)

    # Process last section
    if current_section:
        processed = _process_diff_content(current_file, "\n".join(current_section))
        if processed:
            diff_sections.append(processed)

    return "\n\n".join(diff_sections)


# For testing
if __name__ == "__main__":
    engine = OllamaEngine()
    diff = get_diff()
    print(diff)
    for chunk in engine.stream(diff):
        print(chunk, end="", flush=True)
