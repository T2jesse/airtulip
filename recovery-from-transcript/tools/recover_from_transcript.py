"""Replay Write/StrReplace ops from agent transcript onto workspace files."""
import json
import sys
from pathlib import Path

TRANSCRIPT = Path(
    r"C:\Users\jfxjl\.cursor\projects\c-Users-jfxjl-Desktop-Airtulip"
    r"\agent-transcripts\5119fc50-13f7-4856-9cfc-727df502c309"
    r"\5119fc50-13f7-4856-9cfc-727df502c309.jsonl"
)
ROOT = Path(__file__).resolve().parents[1]

# Optional path filters (substring match, lowercase). Empty = all airtulip project files.
FILTERS = tuple(a.lower() for a in sys.argv[1:]) if len(sys.argv) > 1 else ()


def rel_path(raw: str) -> str | None:
    p = raw.replace("\\", "/")
    low = p.lower()
    marker = "/airtulip/"
    if marker in low:
        return p[low.index(marker) + len(marker) :]
    if low.startswith("c:/users/") and "airtulip/" in low:
        return low.split("airtulip/", 1)[1]
    if not p.startswith("c:") and "/" in p:
        return p.lstrip("/")
    return None


def should_include(rel: str) -> bool:
    if not rel:
        return False
  skip = ("tools/recover", ".cursor/", "node_modules/", "agent-transcripts/")
    if any(s in rel.replace("\\", "/") for s in skip):
        return False
    if not FILTERS:
        return True
    r = rel.lower()
    return any(f in r for f in FILTERS)


# Collect ops in order per file
ops_by_file: dict[str, list] = {}
applied = failed = 0

for line in TRANSCRIPT.read_text(encoding="utf-8").splitlines():
    try:
        o = json.loads(line)
    except json.JSONDecodeError:
        continue
    for part in o.get("message", {}).get("content", []):
        if part.get("type") != "tool_use":
            continue
        inp = part.get("input", {})
        rel = rel_path(inp.get("path", ""))
        if not should_include(rel):
            continue
        name = part.get("name", "")
        if name not in ("Write", "StrReplace"):
            continue
        ops_by_file.setdefault(rel, []).append((name, inp))

# Apply ops per file
for rel, ops in sorted(ops_by_file.items()):
    fp = ROOT / rel.replace("/", "\\")
    content = fp.read_text(encoding="utf-8") if fp.exists() else ""
    file_applied = file_failed = 0
    for name, inp in ops:
        if name == "Write":
            content = inp.get("contents", content)
            file_applied += 1
        elif name == "StrReplace":
            old = inp.get("old_string")
            new = inp.get("new_string", "")
            if old is None:
                continue
            if old not in content:
                file_failed += 1
                continue
            if inp.get("replace_all"):
                content = content.replace(old, new)
            else:
                content = content.replace(old, new, 1)
            file_applied += 1
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(content, encoding="utf-8")
    applied += file_applied
    failed += file_failed
    print(f"{rel}: {len(content.splitlines())} lines, +{file_applied} ok, {file_failed} miss")

print(f"TOTAL: {len(ops_by_file)} files, {applied} ops applied, {failed} ops failed (old_string not found)")
