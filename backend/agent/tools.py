from typing import Any, Callable, Dict, List

from rag.retriever import Retriever
from rag.context_builder import build_context
from ingestion.embedder import embed_texts
from mcp_tools import repo_tools


class ToolsRegistry:
    def __init__(self) -> None:
        self.tools: Dict[str, Callable[[str], str]] = {}

    def register(self, name: str, fn: Callable[[str], str]) -> None:
        self.tools[name] = fn

    def call(self, name: str, arg: str) -> str:
        if name not in self.tools:
            raise KeyError(f"Unknown tool: {name}")
        return self.tools[name](arg)


registry = ToolsRegistry()


# ---- Example stub tool implementations ----
def repo_read_file(self, rel_path: str) -> Dict[str, Any]:
    """
    Read file contents from repository.
    """
    content = repo_tools.read_file(rel_path)
    return {"path": rel_path, "content": content}
def repo_list_files(self, glob_pattern: str) -> Dict[str, Any]:
    """
    List files under the repo matching a glob pattern (e.g., '**/*.py').
    """
    files = repo_tools.list_files(glob_pattern or "**/*.py")
    return {"glob": glob_pattern, "files": files}
def repo_search_code(self, query: str) -> Dict[str, Any]:
    """
    Search code for a string and return top matches.
    """
    hits = repo_tools.search_code(query)
    return {"query": query, "hits": hits}
def repo_apply_patch(self, patch_text: str) -> Dict[str, Any]:
    """
    Apply patch to repo using 'patch -p1'.
    """
    result = repo_tools.apply_patch(patch_text)
    return {"patch": patch_text, **result}
def repo_run_tests(self, command: str) -> Dict[str, Any]:
    """
    Run tests (default 'pytest -q' if command is empty).
    """
    cmd = command or "pytest -q"
    result = repo_tools.run_tests(cmd)
    return {"command": cmd, **result}


# Register tools with the allowed names the planner knows about
registry.register("repo_read_file", repo_read_file)
registry.register("repo_list_files", repo_list_files)
registry.register("repo_search_code", repo_search_code)
registry.register("repo_apply_patch", repo_apply_patch)
registry.register("repo_run_tests", repo_run_tests)
