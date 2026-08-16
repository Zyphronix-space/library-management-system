import importlib
import sys


def go_to(module_name: str) -> None:
    """Open another screen module.

    Every screen file runs its GUI-building code at module import time.
    A plain `import module_name` only executes that code the FIRST time a
    module is imported — Python caches it in sys.modules after that, so
    revisiting a screen a second time in the same run silently does
    nothing (no new window opens, and since the previous window was just
    destroyed, the whole app appears to close). Reloading an
    already-imported module forces its top-level code to run again.
    """
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    else:
        importlib.import_module(module_name)
