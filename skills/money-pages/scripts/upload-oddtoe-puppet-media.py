#!/usr/bin/env python3
"""Upload the two marionette renders for the Oddtoe Puppet Designer page.

Both are Otto's own Midjourney renders from 8 Sep 2026 (the "hand gripping a slender
wooden control" set) in Marketing/Oddtoe New Growth Pages 2026/. The 2048px upscale is
the page hero; the 1024px square is the first carousel slide.
Alt text names no client and no event, per the money-pages rule.
"""
import base64, json, os, pathlib, urllib.request

REPO = pathlib.Path(__file__).resolve().parents[3]
for line in (REPO / '.env').read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

FOLDER = ('/Users/Ottinger/Documents/Oddtoe - iCloud Apple/Marketing/Oddtoe New Growth Pages 2026')
SITE = 'https://www.oddtoe.com'
auth = 'Basic ' + base64.b64encode(
    f"{os.environ['WP_ODDTOE_USER']}:{os.environ['WP_ODDTOE_APP_PASSWORD']}".encode()).decode()
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'

PLAN = [
    ('oddtoe_Close_detail_of_a_hand_gripping_a_slender_wooden_control_56024a6f-c012-4c12-a24b-5eb6e17bf211.png',
     'oddtoe-marionette-head-control-bar-strings.png',
     'Carved marionette head on a control bar, strings running to the hand working it',
     'Marionette head on a control bar'),
    ('oddtoe_Close_detail_of_a_hand_gripping_a_slender_wooden_contr_bc8162d1-e5f4-4181-9d7f-0bf95c7b3527_3.png',
     'oddtoe-marionette-hinged-jaw-strings-hand.png',
     'Marionette with a hinged jaw hanging on strings, a hand below holding a control stick',
     'Marionette on strings with a hinged jaw'),
]

out = {}
for src, filename, alt, title in PLAN:
    data = open(os.path.join(FOLDER, src), 'rb').read()
    req = urllib.request.Request(SITE + '/wp-json/wp/v2/media', data=data, method='POST', headers={
        'Content-Type': 'image/png', 'Content-Disposition': f'attachment; filename="{filename}"',
        'Authorization': auth, 'User-Agent': UA})
    with urllib.request.urlopen(req) as r:
        d = json.load(r)
    mid = d['id']
    meta = json.dumps({'alt_text': alt, 'title': title}).encode()
    req2 = urllib.request.Request(SITE + f'/wp-json/wp/v2/media/{mid}', data=meta, method='POST',
                                  headers={'Content-Type': 'application/json',
                                           'Authorization': auth, 'User-Agent': UA})
    with urllib.request.urlopen(req2) as r:
        json.load(r)
    out[filename] = mid
    print(mid, filename, '-', alt)

print(json.dumps(out, indent=2))
