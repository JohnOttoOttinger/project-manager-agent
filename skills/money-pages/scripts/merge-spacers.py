#!/usr/bin/env python3
"""Merge consecutive dfd_spacer shortcodes (sum sizes per breakpoint). Pixel-identical output."""
import re, json, os, urllib.request, base64, sys, pathlib

SPACER = re.compile(r'\[dfd_spacer([^\]]*)\]')
ATTR = re.compile(r'(\w+)="([^"]*)"')
RES_KEYS = ['screen_wide_resolution', 'screen_normal_resolution', 'screen_tablet_resolution', 'screen_mobile_resolution']
SIZE_KEYS = ['screen_wide_spacer_size', 'screen_normal_spacer_size', 'screen_tablet_spacer_size', 'screen_mobile_spacer_size']

def parse(tag_attrs):
    d = dict(ATTR.findall(tag_attrs))
    if not all(k in d for k in RES_KEYS + SIZE_KEYS):
        return None
    if any(not d[k].isdigit() for k in SIZE_KEYS):
        return None
    return d

def build(res, sums):
    return ('[dfd_spacer screen_wide_resolution="%s" screen_wide_spacer_size="%d" screen_normal_resolution="%s" '
            'screen_tablet_resolution="%s" screen_mobile_resolution="%s" screen_normal_spacer_size="%d" '
            'screen_tablet_spacer_size="%d" screen_mobile_spacer_size="%d"]') % (
        res[0], sums[0], res[1], res[2], res[3], sums[1], sums[2], sums[3])

def merge(content):
    matches = list(SPACER.finditer(content))
    out, pos, i, merged_runs = [], 0, 0, 0
    while i < len(matches):
        m = matches[i]
        # collect a run of consecutive spacers separated only by whitespace
        run = [m]
        j = i + 1
        while j < len(matches) and content[run[-1].end():matches[j].start()].strip() == '':
            run.append(matches[j]); j += 1
        parsed = [parse(x.group(1)) for x in run]
        # mergeable subrun: all parsed, identical resolutions
        if len(run) > 1 and all(parsed) and len({tuple(p[k] for k in RES_KEYS) for p in parsed}) == 1:
            res = [parsed[0][k] for k in RES_KEYS]
            sums = [sum(int(p[k]) for p in parsed) for k in SIZE_KEYS]
            out.append(content[pos:run[0].start()])
            out.append(build(res, sums))
            pos = run[-1].end()
            merged_runs += 1
            i = j
        else:
            i = j if len(run) > 1 else i + 1
    out.append(content[pos:])
    return ''.join(out), merged_runs

def totals(content):
    t = [0, 0, 0, 0]
    for m in SPACER.finditer(content):
        p = parse(m.group(1))
        if p:
            for k, key in enumerate(SIZE_KEYS):
                t[k] += int(p[key])
    return t

def strip_spacers(content):
    return re.sub(r'\s+', '', SPACER.sub('', content))

def process(content):
    new, runs = merge(content)
    assert totals(content) == totals(new), 'SPACING TOTALS CHANGED — aborting'
    assert strip_spacers(content) == strip_spacers(new), 'NON-SPACER CONTENT CHANGED — aborting'
    before = len(SPACER.findall(content)); after = len(SPACER.findall(new))
    return new, before, after, runs

if __name__ == '__main__':
    auth = {}
    for brand, prefix in [('datalabs', 'WP_DATALABS'), ('oddtoe', 'WP_ODDTOE')]:
        auth[brand] = 'Basic ' + base64.b64encode(
            f"{os.environ[prefix + '_USER']}:{os.environ[prefix + '_APP_PASSWORD']}".encode()).decode()
    UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    SITES = {'datalabs': 'https://www.datalabsagency.com', 'oddtoe': 'https://www.oddtoe.com'}

    def req(brand, pid, data=None):
        r = urllib.request.Request(
            f'{SITES[brand]}/wp-json/wp/v2/pages/{pid}' + ('' if data else '?context=edit&nc=sp'),
            data=json.dumps(data).encode() if data else None,
            headers={'Authorization': auth[brand], 'User-Agent': UA, 'Content-Type': 'application/json'},
            method='POST' if data else 'GET')
        return json.load(urllib.request.urlopen(r))

    pages = [('datalabs', 52964, 'Datalabs MASTER'), ('datalabs', 52962, 'Workshop pricing (live)'),
             ('oddtoe', 16132, 'Oddtoe MASTER'), ('oddtoe', 16133, 'Activation ideas (live)'),
             ('oddtoe', 16134, 'AI animation (live)')]
    for brand, pid, label in pages:
        raw = req(brand, pid)['content']['raw']
        new, before, after, runs = process(raw)
        if before == after:
            print(f'{label} ({pid}): no consecutive runs to merge ({before} spacers)')
            continue
        req(brand, pid, {'content': new})
        check = req(brand, pid)['content']['raw']
        ok = totals(check) == totals(raw)
        print(f'{label} ({pid}): {before} -> {after} spacers ({runs} runs merged) | totals preserved on server: {ok}')

    for f in ['skills/money-pages/references/design-kit.html', 'skills/money-pages/references/design-kit-oddtoe.html']:
        p = pathlib.Path(f)
        c = p.read_text()
        new, before, after, runs = process(c)
        p.write_text(new)
        print(f'{f}: {before} -> {after} spacers ({runs} runs merged)')
