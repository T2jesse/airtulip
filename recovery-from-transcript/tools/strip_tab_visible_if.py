import re
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "sections"
pat = re.compile(
    r'^\s*"visible_if": "\{\{ block\.settings\.tab_count.*\}\}",\s*\n',
    re.M,
)
for name in ("main-product.liquid", "featured-product.liquid", "main-product-modal.liquid"):
    path = root / name
    text = path.read_text(encoding="utf-8")
    path.write_text(pat.sub("", text), encoding="utf-8")
    print(f"{name}: removed {len(pat.findall(text))}")
