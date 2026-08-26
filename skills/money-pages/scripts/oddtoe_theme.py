#!/usr/bin/env python3
"""Per-page dark tints for Oddtoe money pages.

The kit ships plum (#26161f). Otto called the repetition across pages tired on
26 Aug 2026, so each money page now carries its own near-black, the way the
Datalabs Visual Case Studies do (vcs_lib.apply_theme).

A money page carries the plum in four places, plus one leftover:
  1. Page Options  crum_page_custom_bg_color   <- wp-admin, not in the content
  2. hero row      dfd_overlay_color
  3. three rows    css=".vc_custom_N{background-color: ...}"  (redundant with 1)
  4. table rows    border-bottom: 1px solid ...
  5. the scroll-down delimiter's lavender line + icon, inherited from the v0 seed

retint() handles 2-5. Row backgrounds are STRIPPED rather than recoloured so the
page ground stays the single source of truth for the tint (same call vcs_lib
makes). Set 1 in wp-admin Page Options.
"""
import re, sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from vcs_lib import lighten  # noqa: E402

KIT_PLUM = '#26161f'
SAND = '#ddccb1'
OLIVE = '#8a8f6a'

# Otto-approved 26 Aug 2026. Assign one per page; don't repeat a tint on
# neighbouring pages in the same cluster.
PALETTE = {
    'plum':      '#26161f',   # kit default
    'teal':      '#142322',
    'ink':       '#171d2a',
    'forest':    '#16211a',
    'graphite':  '#1c1c1f',
    'umber':     '#241b16',
    'slate':     '#1a1e26',
    'nearblack': '#101418',
}


def retint(page, bg, old=KIT_PLUM):
    """Return (retinted_page, notes). bg is a hex or a PALETTE key."""
    bg = PALETTE.get(bg, bg)
    hair = lighten(bg, 0.13)          # table hairlines, a touch above the ground
    line = lighten(bg, 0.18) + '1C'   # delimiter rule, keeping the kit's 11% alpha
    notes = []

    def sub(pattern, repl, label, regex=False):
        nonlocal page
        n = len(re.findall(pattern, page)) if regex else page.count(pattern)
        if n:
            page = re.sub(pattern, repl, page) if regex else page.replace(pattern, repl)
            notes.append(f'{label}: {n}')

    sub(f'dfd_overlay_color="{old}"', f'dfd_overlay_color="{bg}"', 'hero overlay')
    sub(f'border-bottom: 1px solid {old} !important',
        f'border-bottom: 1px solid {hair} !important', f'table hairlines -> {hair}')
    sub(r'\s*css="\.vc_custom_\d+\{background-color: ' + re.escape(old) + r' !important;\}"',
        '', 'row backgrounds stripped', regex=True)
    sub('delim_line_color="#8224E31C"', f'delim_line_color="{line}"', 'delimiter rule (was lavender)')
    sub('icon_color="#EEE6F6"', f'icon_color="{SAND}"', 'delimiter icon -> sand')
    sub('icon_hover_color="#D4C9E0"', f'icon_hover_color="{OLIVE}"', 'delimiter icon hover -> olive')

    left = page.count(old)
    if left:
        notes.append(f'WARNING: {left} unhandled {old} left — inspect before pushing')
    return page, notes
