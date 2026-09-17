#!/usr/bin/env python3
"""Compose a Use Case paid twin and its thank-you page.

    python3 compose-usecase-paid.py references/usecase-content-publicity-stunts.json references/usecase-paid-publicity-stunts.json

Reads the use-case content JSON (hero, circles, package, FAQ, portfolio) and the paid overlay
(ad headline, CTA, form id, thank-you copy). Fills design-kit-oddtoe-usecase-paid.html and
design-kit-oddtoe-usecase-thanks.html the same way compose-usecase.py does, and writes
references/composed/usecase-<slug>-paid-<date>.html and usecase-<slug>-thanks-<date>.html.
Draft only; never sends anything to WordPress.
"""
from __future__ import annotations
import datetime, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from compose_usecase_lib import REFS, enc, faq_sections  # noqa

KIT_PAID = REFS / "design-kit-oddtoe-usecase-paid.html"
KIT_THANKS = REFS / "design-kit-oddtoe-usecase-thanks.html"


def fill(kit_path: Path, c: dict) -> str:
    body = re.sub(r"{{([A-Z0-9_]+)}}", lambda m: str(c[m.group(1)]), kit_path.read_text(encoding="utf-8"))
    body = re.sub(r"<!--(?!RAW-->|/RAW-->).*?-->\n?", "", body, flags=re.S)
    body = re.sub(r"<!--RAW-->(.*?)<!--/RAW-->", lambda m: enc(m.group(1)), body, flags=re.S)
    assert "{{" not in body, "unfilled token: " + re.search(r"{{[^}]+}}", body).group(0)
    assert "<!--" not in body, "an HTML comment survived"
    return body.strip()


def main():
    base = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    paid = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    c = dict(base); c.update(paid)
    c.setdefault("HERO_BG_POS", "center center")   # per page: where the hero image sits behind the left-aligned title
    c["ID_SLUG"] = base["ID_SLUG"] + "-go"
    # every link that is not the form is a leak on an ad page: FAQ answers keep their words, lose their anchors
    faq = [{"q": base["FAQ"][i]["q"], "a": re.sub(r"</?a\b[^>]*>", "", base["FAQ"][i]["a"])} for i in paid["FAQ_PICK"]]
    c["FAQ_SECTIONS"] = faq_sections(faq, paid["FAQ_TAB_STAMP"], c["ID_SLUG"])
    date = datetime.date.today().isoformat()
    slug = paid["URL_SLUG"]
    for name, kit in (("paid", KIT_PAID), ("thanks", KIT_THANKS)):
        body = fill(kit, c)
        out = REFS / "composed" / f"usecase-{slug}-{name}-{date}.html"
        out.write_text(body, encoding="utf-8")
        print(f"composed: {out.relative_to(REFS.parent)}  {len(body)} chars, {body.count('[vc_row ')} rows, {body.count('[vc_raw_html]')} raw blocks")
    print(f"PAGE SETTINGS (wp-admin), both pages: template page-custom.php · parent {paid['PARENT_PAGE_ID']} · "
          f"Custom bg {c['TINT']} · header style without menu · Yoast: noindex, nofollow, exclude from sitemap")
    print(f"twin slug: /use-cases/{slug}/go/   canonical → /use-cases/{slug}/   Yoast title: {paid['YOAST_TITLE_TWIN']}")
    print(f"thanks slug: /use-cases/{slug}/thanks/   Yoast title: {paid['YOAST_TITLE_THANKS']}")
    print(f"Gravity form {paid['FORM_ID']} confirmation: redirect to https://www.oddtoe.com/use-cases/{slug}/thanks/")
    print("Meta: custom conversion on URL contains /thanks/, or the Lead event the page fires. Campaign objective: Leads → website.")


if __name__ == "__main__":
    main()
