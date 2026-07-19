from pathlib import Path
import pytest


def test_tailwind_compiled_up_to_date():
    root = Path.cwd()
    public_css = root / 'public' / 'tailwind.css'
    styles = root / 'styles.css'
    config = root / 'tailwind.config.js'

    assert public_css.exists(), "public/tailwind.css is missing — run `npm run build:tailwind`"

    public_mtime = public_css.stat().st_mtime
    styles_mtime = styles.stat().st_mtime if styles.exists() else 0
    config_mtime = config.stat().st_mtime if config.exists() else 0

    assert public_mtime >= styles_mtime, (
        "public/tailwind.css is older than styles.css — recompile with `npm run build:tailwind`"
    )
    assert public_mtime >= config_mtime, (
        "public/tailwind.css is older than tailwind.config.js — recompile with `npm run build:tailwind`"
    )
