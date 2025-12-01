from typing import Callable, Dict


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
def repo_read_file_tool(path: str) -> str:
    """Very simple file reader tool. Path is relative to backend root."""
    import os

    try:
        # You can adjust the base dir if needed
        full_path = os.path.abspath(path)
        with open(full_path, "r") as f:
            return f"Contents of {full_path}:\n\n" + f.read()
    except Exception as e:
        return f"[repo_read_file] Failed to read {path}: {e}"


def repo_run_tests_tool(_: str) -> str:
    """Stub for running tests. Extend later to actually run pytest or similar."""
    # You can later implement subprocess.run(["pytest", "-q"], ...)
    return "[repo_run_tests] Test runner not implemented yet."


def repo_apply_patch_tool(_: str) -> str:
    """Stub for applying patches."""
    return "[repo_apply_patch] Patch application not implemented yet."


# Register tools with the allowed names the planner knows about
registry.register("repo_read_file", repo_read_file_tool)
registry.register("repo_run_tests", repo_run_tests_tool)
registry.register("repo_apply_patch", repo_apply_patch_tool)
