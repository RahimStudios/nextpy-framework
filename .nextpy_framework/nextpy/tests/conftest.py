import sys
from pathlib import Path

# Ensure the framework package is importable and the JSX import hook is
# installed before any test module (some contain JSX syntax) is imported.
_framework = Path(__file__).resolve().parents[2]
if str(_framework) not in sys.path:
    sys.path.insert(0, str(_framework))
try:
    import nextpy.jsx_transformer  # noqa: F401  (installs the import hook)
except Exception:
    pass
