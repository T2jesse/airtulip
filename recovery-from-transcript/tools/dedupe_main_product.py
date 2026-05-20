from pathlib import Path

p = Path(__file__).resolve().parents[1] / "sections" / "main-product.liquid"
t = p.read_text(encoding="utf-8")
marker = '      "type": "tabbed_content",'
countdown = '      "type": "countdown",'

first = t.find(marker)
second = t.find(marker, first + 1)
cd = t.find(countdown, first)

if second == -1 or second >= cd:
    print("No duplicate tabbed_content blocks found.")
else:
    p.write_text(t[:second] + t[cd:], encoding="utf-8")
    print(f"Removed duplicate schema blocks. Lines: {len(t.splitlines())} -> {len((t[:second] + t[cd:]).splitlines())}")
