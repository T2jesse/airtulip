"""Replay theme.css StrReplace/Write ops from agent transcript."""
import json
from pathlib import Path

transcript = Path(
    r"C:\Users\jfxjl\.cursor\projects\c-Users-jfxjl-Desktop-Airtulip"
    r"\agent-transcripts\5119fc50-13f7-4856-9cfc-727df502c309"
    r"\5119fc50-13f7-4856-9cfc-727df502c309.jsonl"
)
theme_path = Path(__file__).resolve().parents[1] / "assets" / "theme.css"
content = theme_path.read_text(encoding="utf-8")
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
        p = inp.get("path", "").replace("\\", "/").lower()
        if not p.endswith("assets/theme.css"):
            continue
        name = part.get("name", "")
        if name == "Write":
            content = inp.get("contents", content)
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
            applied += 1

theme_path.write_text(content, encoding="utf-8")
print(f"lines: {len(content.splitlines())}")
print(f"applied: {applied}, failed: {failed}")
