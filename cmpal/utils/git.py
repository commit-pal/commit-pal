import subprocess
from typing import List, Optional

from cmpal.inference.llm import OllamaEngine


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
    # TODO: Cleanup diff to shorten context length (eg: poetry.lock)
    try:
        cmd = ["git", "diff", "--cached", "--color=never"]
        if file_path:
            cmd.append(file_path)

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


if __name__ == "__main__":
    engine = OllamaEngine()
    diff = get_diff()
    for chunk in engine.stream(diff):
        print(chunk, end="", flush=True)
