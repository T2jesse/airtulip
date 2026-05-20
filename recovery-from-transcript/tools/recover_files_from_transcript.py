"""Replay StrReplace/Write ops from agent transcript for given paths."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
transcript = Path(
    r"C:\Users\jfxjl\.cursor\projects\c-Users-jfxjl-Desktop-Airtulip"
    r"\agent-transcripts\5119fc50-13f7-4856-9cfc-727df502c309"
    r"\5119fc50-13f7-4856-9cfc-727df502c309.jsonl"
)

prefixes = tuple(
    p.replace("\\", "/").lower()
    for p in sys.argv[1:]
) or ("sections/", "snippets/section-heading.liquid", "snippets/product-tabbed-content.liquid")


def norm(p: str) -> str:
    return p.replace("\\", "/").lower()


def matches(path: str) -> bool:
    p = norm(path)
    if not p.startswith("c:"):
        idx = p.find("/airtulip/")
        if idx >= 0:
            p = p[idx + len("/airtulip/") :]
    for pref in prefixes:
        if p.endswith(pref) or pref in p:
            return True
    return False


files: dict[str, str] = {}
applied = failed = 0

for line in transcript.read_text(encoding="utf-8").splitlines():
    try:
        o = json.loads(line)
    except json.JSONDecodeError:
        continue
    for part in o.get("message", {}).get("content", []):
        if part.get("type") != "tool_use":
            continue
        inp = part.get("input", {})
        path = inp.get("path", "")
        if not path or not matches(path):
            continue
        rel = path.replace("\\", "/")
        if "airtulip/" in rel.lower():
            rel = rel.split("airtulip/", 1)[-1]
        key = rel
        if key not in files:
            fp = ROOT / rel
            if fp.exists():
                files[key] = fp.read_text(encoding="utf-8")
            else:
                files[key] = ""
        content = files[key]
        name = part.get("name", "")
        if name == "Write":
            files[key] = inp.get("contents", content)
            applied += 1
        elif name == "StrReplace":
            old = inp.get("old_string")
            new = inp.get("new_string", "")
            if old is None:
                continue
            if old not in content:
                failed += 1
                continue
            if inp.get("replace_all"):
                content = content.replace(old, new)
            else:
                content = content.replace(old, new, 1)
            files[key] = content
            applied += 1

for rel, content in files.items():
    fp = ROOT / rel
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(content, encoding="utf-8")
    print(f"wrote {rel} ({len(content.splitlines())} lines)")

print(f"files: {len(files)}, applied: {applied}, failed: {failed}")
