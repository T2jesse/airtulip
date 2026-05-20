"""Remove duplicate CSS blocks introduced by transcript replay (keeps first copy)."""
from pathlib import Path

CSS = Path(__file__).resolve().parents[1] / "assets" / "theme.css"

MARKERS = (
    "/*! section--rounded-contained:",
    "/* Lateral PDP / quick-view tabs",
)


def dedupe_by_marker(text: str, marker: str) -> tuple[str, int]:
    removed = 0
    first = text.find(marker)
    if first < 0:
        return text, 0

    while True:
        second = text.find(marker, first + len(marker))
        if second < 0:
            break
        # End at next marker of any type, or EOF
        end = len(text)
        for m in MARKERS:
            if m == marker:
                continue
            pos = text.find(m, second + len(marker))
            if pos > second and pos < end:
                end = pos
        # Also stop at footer-group if rounded-contained dup runs into normal CSS
        if marker.startswith("/*! section--rounded-contained"):
            fg = text.find("\n.footer-group .section--next-rounded", second)
            if fg > second and fg < end:
                end = fg
        if marker.startswith("/* Lateral PDP"):
            nxt = text.find("\n/* Homepage + PDP section headings", second)
            if nxt > second and nxt < end:
                end = nxt
        text = text[:second] + text[end:]
        removed += 1

    return text, removed


def main() -> None:
    original = CSS.read_text(encoding="utf-8")
    text = original
    total = 0
    for marker in MARKERS:
        text, n = dedupe_by_marker(text, marker)
        total += n
        if n:
            print(f"  removed {n} duplicate(s) of {marker[:50]}...")

  # Collapse excessive blank lines from removals
    while "\n\n\n\n" in text:
        text = text.replace("\n\n\n\n", "\n\n\n")

    CSS.write_text(text, encoding="utf-8", newline="\n")
    before = original.count("\n") + 1
    after = text.count("\n") + 1
    print(f"theme.css: {before} -> {after} lines ({total} duplicate blocks removed)")


if __name__ == "__main__":
    main()
