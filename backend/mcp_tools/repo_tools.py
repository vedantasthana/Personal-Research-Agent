import subprocess
from pathlib import Path
from typing import List, Dict

# Adjust if your repo layout changes
REPO_ROOT = Path(__file__).resolve().parents[2]


def _safe_join(rel_path: str) -> Path:
    """
    Join a relative path to the repo root and ensure it stays inside.
    """
    target = (REPO_ROOT / rel_path).resolve()
    if not str(target).startswith(str(REPO_ROOT)):
        raise ValueError(f"Path escapes repository root: {rel_path}")
    return target


def read_file(rel_path: str) -> str:
    """
    Read a text file from the repository by relative path.
    """
    path = _safe_join(rel_path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: {rel_path}")
    return path.read_text(encoding="utf-8", errors="ignore")


def list_files(glob_pattern: str = "**/*.py") -> List[str]:
    """
    List files matching a glob pattern, relative to repository root.
    Default: all Python files.
    """
    paths = REPO_ROOT.glob(glob_pattern)
    return [p.relative_to(REPO_ROOT).as_posix() for p in paths if p.is_file()]


def search_code(query: str, glob_pattern: str = "**/*.py", max_hits: int = 20) -> List[Dict]:
    """
    Very simple code search: grep for query in matching files.
    Returns a list of {path, line_no, line}.
    """
    hits: List[Dict] = []
    for rel in list_files(glob_pattern):
        path = _safe_join(rel)
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f, start=1):
                    if query in line:
                        hits.append(
                            {
                                "path": rel,
                                "line_no": i,
                                "line": line.rstrip("\n"),
                            }
                        )
                        if len(hits) >= max_hits:
                            return hits
        except Exception:
            # Ignore unreadable files
            continue
    return hits


def apply_patch(patch_text: str) -> Dict[str, str]:
    """
    Apply a unified diff patch (as produced by git diff -u).
    Returns stdout & stderr.
    """
    process = subprocess.Popen(
        ["patch", "-p1"],
        cwd=str(REPO_ROOT),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = process.communicate(input=patch_text)
    return {"stdout": out, "stderr": err, "returncode": str(process.returncode)}


def run_tests(command: str = "pytest -q") -> Dict[str, str]:
    """
    Run tests (default: pytest -q) from the repo root.
    """
    process = subprocess.Popen(
        command.split(),
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = process.communicate()
    return {"stdout": out, "stderr": err, "returncode": str(process.returncode)}
