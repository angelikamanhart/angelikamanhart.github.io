"""Update PRESET_POSITIONS in publications.html from clipboard.

Usage:
    1. Open publications.html, toggle the co-authorship network
    2. Drag nodes to desired positions
    3. Click "Export Layout" (copies JSON to clipboard)
    4. Run: python update_layout.py
"""

import re
import subprocess
import sys


def get_clipboard():
    """Read clipboard text (Windows)."""
    result = subprocess.run(
        ["powershell", "-command", "Get-Clipboard"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def main():
    clipboard = get_clipboard()
    if not clipboard or not clipboard.startswith("{"):
        print("Error: Clipboard doesn't contain valid JSON. Click 'Export Layout' first.")
        sys.exit(1)

    html_path = "publications.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Match the PRESET_POSITIONS block
    pattern = r"(var PRESET_POSITIONS = )\{[^}]*(?:\{[^}]*\}[^}]*)*\};"
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        print("Error: Could not find PRESET_POSITIONS in publications.html")
        sys.exit(1)

    new_block = "var PRESET_POSITIONS = " + clipboard + ";"
    html = html[:match.start()] + new_block + html[match.end():]

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Count entries
    import json
    positions = json.loads(clipboard)
    print(f"Updated PRESET_POSITIONS with {len(positions)} entries in {html_path}.")


if __name__ == "__main__":
    main()
