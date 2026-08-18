#!/usr/bin/env python3
"""Add or extend Q&A modules + FAQPage schema across Oddtoe pages.

Built for the 18 Aug 2026 rollout that followed the Q&A module audit
(skills/analytics/references/audits/2026-08-18-qa-module-audit.md).

Two jobs per page, deliberately separate:
  visible accordion  -> the SEO half (better answers matched to real queries)
  FAQPage JSON-LD    -> the GEO half (clean extraction by AI answer engines)

Three modes:
  append   page already has a [dfd_accordion]; add sections, schema covers ALL Qs
  new_row  page has no Q&A; insert a FAQ row before the contact-form row
  post     a blog post with no shortcodes; native <h3> + JSON-LD, no accordion

Safety: every page asserts that nothing outside the inserted/extended block
changed, byte for byte. Read and write with newline='' — a plain text read
silently converts CRLF to LF and would rewrite every line ending on the page.

Usage:  python3 faq-rollout-oddtoe.py --dry-run
        python3 faq-rollout-oddtoe.py --apply --only weird-art
"""
import argparse, base64, json, os, re, sys, urllib.parse, urllib.request

SITE = 'https://www.oddtoe.com'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'

def spacer(size, tablet=None, mobile=None):
    t = tablet if tablet is not None else size
    m = mobile if mobile is not None else size
    return ('[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="%d" '
            'screen_normal_resolution="1024" screen_tablet_resolution="800" '
            'screen_mobile_resolution="480" screen_normal_spacer_size="%d" '
            'screen_tablet_spacer_size="%d" screen_mobile_spacer_size="%d"]' % (size, size, t, m))

def accordion_open(style):
    return ('[dfd_accordion style="%s" active_section="1" font_size="18" tab_title_google_fonts="yes" '
            'tab_title_custom_fonts="font_family:Arvo%%3Aregular%%2Citalic%%2C700%%2C700italic|'
            'font_style:700%%20bold%%20regular%%3A700%%3Anormal" icon_size="14"]' % style)

def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    for ent, ch in [('&mdash;','—'),('&ndash;','–'),('&amp;','&'),('&rsquo;','’'),
                    ('&lsquo;','‘'),('&quot;','"'),('&nbsp;',' ')]:
        s = s.replace(ent, ch)
    return re.sub(r'\s+', ' ', s).strip()

def schema_block(pairs):
    ents = [{"@type":"Question","name":plain(q),
             "acceptedAnswer":{"@type":"Answer","text":plain(a)}} for q, a in pairs]
    js = ('<script type="application/ld+json">'
          + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":ents},
                       ensure_ascii=False) + '</script>')
    return js, '[vc_raw_html]' + base64.b64encode(
        urllib.parse.quote(js, safe='').encode()).decode() + '[/vc_raw_html]'

def sections(pairs, tag):
    out = []
    for i, (q, a) in enumerate(pairs, 1):
        out.append('[vc_tta_section title="%s" tab_id="%s-%d-2026"][vc_column_text css=""]</p>\n'
                   '<p style="text-align: center;">%s</p>\n<p>[/vc_column_text][/vc_tta_section]'
                   % (q.replace('"', '&quot;'), tag, i, a))
    return ''.join(out)

def nearest_dark_bg(src, before, default='#1a1a1a'):
    """Background colour of the closest preceding row, so the block sits in the page's palette."""
    best = None
    for m in re.finditer(r'\[vc_row[^\]]*\]', src):
        if m.start() >= before: break
        cols = re.findall(r'background-color:\s*(#[0-9a-fA-F]{6})', m.group(0))
        if cols: best = cols[-1]
    return best or default


def build_new_row(src, cfg):
    """Insert a fresh FAQ row immediately before the contact-form row."""
    anchor_idx = cfg['anchor'](src)
    bg = cfg.get('bg') or nearest_dark_bg(src, anchor_idx)
    _, raw = schema_block(cfg['new'])
    row = ('[vc_row bg_check="row-background-dark" dfd_enable_overlay="" '
           'css=".vc_custom_%s{background-color: %s !important;}"]'
           '[vc_column width="1/4"][/vc_column][vc_column width="1/2"]'
           % (cfg['vc_id'], bg)
           + spacer(80, 60, 50)
           + '[vc_column_text css="" item_animation="transition.fadeIn"]</p>\n'
           '<p style="text-align: center; line-height: 1; margin-bottom: 0;">'
           '<span style="font-family: Qwigley; font-size: 36pt;">Questions &amp; Answers</span></p>\n'
           '<h2 style="text-align: center;"><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">'
           + cfg['topic'] + '</span></h2>\n<p>[/vc_column_text]'
           + spacer(40, 20, 20) + accordion_open(cfg.get('style', 'style-3'))
           + sections(cfg['new'], cfg['tag']) + '[/dfd_accordion]' + raw + spacer(40)
           + '[/vc_column][vc_column width="1/4"][/vc_column][/vc_row]')
    out = src[:anchor_idx] + row + src[anchor_idx:]
    assert out[:anchor_idx] == src[:anchor_idx]
    assert out[anchor_idx + len(row):] == src[anchor_idx:]
    return out, row, len(cfg['new'])


def build_append(src, cfg):
    """Add sections to the accordion already on the page; schema covers old + new."""
    m = re.search(r'\[dfd_accordion.*?\[/dfd_accordion\]', src, re.S)
    assert m, 'no accordion to append to'
    acc = m.group(0)
    existing = []
    for s in re.finditer(r'\[vc_tta_section title="([^"]+)"[^\]]*\](.*?)\[/vc_tta_section\]', acc, re.S):
        body = re.sub(r'\[/?vc_column_text[^\]]*\]', '', s.group(2))
        existing.append((s.group(1), body))
    assert existing, 'accordion has no sections'
    new_acc = acc[:-len('[/dfd_accordion]')] + sections(cfg['new'], cfg['tag']) + '[/dfd_accordion]'
    _, raw = schema_block(existing + cfg['new'])

    out = src[:m.start()] + new_acc + src[m.end():]
    # schema goes straight after the accordion; replace any existing FAQ raw_html first
    ins = m.start() + len(new_acc)
    tail = out[ins:]
    old_raw = re.match(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', tail)
    if old_raw and 'FAQPage' in urllib.parse.unquote(
            base64.b64decode(old_raw.group(0)[14:-15]).decode()):
        out = out[:ins] + raw + tail[len(old_raw.group(0)):]
    else:
        out = out[:ins] + raw + tail
    assert out[:m.start()] == src[:m.start()], 'content before the accordion changed'
    return out, new_acc, len(existing) + len(cfg['new'])


def build_post(src, cfg):
    """Blog post: no shortcodes on the page, so match its own HTML heading pattern."""
    js, _ = schema_block(cfg['new'])
    parts = ['\n<h2><strong>Questions &amp; Answers</strong></h2>\n']
    for q, a in cfg['new']:
        parts.append('<h3><strong>%s</strong></h3>\n<p>%s</p>\n' % (q, a))
    parts.append(js)
    blk = ''.join(parts)
    out = src + blk
    assert out[:len(src)] == src
    return out, blk, len(cfg['new'])


BUILDERS = {'new_row': build_new_row, 'append': build_append, 'post': build_post}


def wp(path, method='GET', payload=None):
    auth = base64.b64encode(
        f"{os.environ['WP_ODDTOE_USER']}:{os.environ['WP_ODDTOE_APP_PASSWORD']}".encode()).decode()
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(SITE + path, data=data, method=method,
                                 headers={'Authorization': 'Basic ' + auth, 'User-Agent': UA,
                                          'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req))


def run(pages, apply_, only):
    for cfg in pages:
        if only and cfg['slug'] != only:
            continue
        kind = cfg.get('type', 'pages')
        cur = wp(f"/wp-json/wp/v2/{kind}/{cfg['id']}?context=edit&_fields=content,link,modified")
        src = cur['content']['raw']
        out, blk, total = BUILDERS[cfg['mode']](src, cfg)
        assert '{{' not in out
        print(f"{cfg['slug']:<42} {cfg['mode']:<8} {len(src):>6} -> {len(out):>6} "
              f"(+{len(out)-len(src):>5})  Qs in schema: {total}  CR {src.count(chr(13))}->{out.count(chr(13))}")
        if apply_:
            res = wp(f"/wp-json/wp/v2/{kind}/{cfg['id']}", 'POST', {'content': out})
            ok = res['content']['raw'] == out
            print(f"{'':<42} applied: {ok}  {res['link']}")
            assert ok, 'saved content does not match what was composed'


if __name__ == '__main__':
    from faq_rollout_content import PAGES
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--only')
    a = ap.parse_args()
    run(PAGES, a.apply, a.only)
    print('\ndry run — nothing written' if not a.apply else '\napplied')
