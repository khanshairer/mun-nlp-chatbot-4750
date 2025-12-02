import os

README_PATH = "README.md"
SCREENSHOT_DIR = "screenshots"
START_MARKER = "<!-- SCREENSHOTS_START -->"
END_MARKER = "<!-- SCREENSHOTS_END -->"

def main():
    # Collect image files (PNG/JPG/GIF) from screenshots/
    if not os.path.isdir(SCREENSHOT_DIR):
        print(f"No '{SCREENSHOT_DIR}' directory found.")
        return

    files = sorted(
        f for f in os.listdir(SCREENSHOT_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    )

    if not files:
        content_block = "_No screenshots found in `screenshots/` yet._"
    else:
        lines = []
        for f in files:
            path = f"{SCREENSHOT_DIR}/{f}"
            title = os.path.splitext(f)[0].replace("-", " ").replace("_", " ").title()
            lines.append(f"**{title}**  ")
            lines.append(f"![{title}]({path})")
            lines.append("")  # blank line between images
        content_block = "\n".join(lines).strip()

    # Read README
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    if START_MARKER not in readme or END_MARKER not in readme:
        print("Markers not found in README. Make sure you added SCREENSHOTS_START/END.")
        return

    # Replace between markers
    before, rest = readme.split(START_MARKER, 1)
    middle, after = rest.split(END_MARKER, 1)

    new_middle = f"{START_MARKER}\n\n{content_block}\n\n{END_MARKER}"
    new_readme = before + new_middle + after

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print(f"Updated screenshots section in {README_PATH} with {len(files)} file(s).")

if __name__ == "__main__":
    main()
