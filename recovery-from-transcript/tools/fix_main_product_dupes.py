import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "sections" / "main-product.liquid"
t = p.read_text(encoding="utf-8")
pat = re.compile(
    r"\{%- when 'shop_pay_installments' -%}\s*"
    r"<div class=\"product__installments\".*?endform -%}\s*"
    r"</div>\s*",
    re.DOTALL,
)
matches = list(pat.finditer(t))
if len(matches) <= 1:
    print(f"found {len(matches)} shop_pay block(s)")
else:
    for m in reversed(matches[1:]):
        t = t[: m.start()] + t[m.end() :]
    p.write_text(t, encoding="utf-8")
    print(f"removed {len(matches) - 1} duplicate(s); lines {len(t.splitlines())}")
