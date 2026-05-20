"""Export the LAST full Write per file from the agent transcript (read-only)."""
import json
from pathlib import Path

TRANSCRIPT = Path(
    r"C:\Users\jfxjl\.cursor\projects\c-Users-jfxjl-Desktop-Airtulip"
    r"\agent-transcripts\5119fc50-13f7-4856-9cfc-727df502c309"
    r"\5119fc50-13f7-4856-9cfc-727df502c309.jsonl"
)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "recovery-from-transcript"


def rel_path(raw: str) -> str | None:
    p = raw.strip().replace("\n", "").replace("\\", "/")
    low = p.lower()
    if "/airtulip/" in low:
        return p[low.index("/airtulip/") + len("/airtulip/") :]
    if low.startswith("c:/users/") and "airtulip/" in low:
        return low.split("airtulip/", 1)[1]
    return None


last_writes: dict[str, str] = {}

for line in TRANSCRIPT.read_text(encoding="utf-8").splitlines():
    try:
        o = json.loads(line)
    except json.JSONDecodeError:
        continue
    for part in o.get("message", {}).get("content", []):
        if part.get("type") != "tool_use" or part.get("name") != "Write":
            continue
        inp = part.get("input", {})
        rel = rel_path(inp.get("path", ""))
        if not rel or not inp.get("contents"):
            continue
        if "recovery-from-transcript" in rel:
            continue
        last_writes[rel] = inp["contents"]

OUT.mkdir(parents=True, exist_ok=True)
for rel, body in sorted(last_writes.items()):
    dest = OUT / rel.replace("/", "\\")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body, encoding="utf-8", newline="\n")

print(f"Exported {len(last_writes)} files to {OUT}")
for rel in sorted(last_writes):
    print(f"  {rel}")
