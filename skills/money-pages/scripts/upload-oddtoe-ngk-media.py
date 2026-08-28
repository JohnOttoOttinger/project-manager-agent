#!/usr/bin/env python3
"""Upload the NGK Flash-showcase captures to oddtoe.com media for the NGK Visual Case Study.

Files come from the curated library (00_Oddtoe-Curated-Library/08_Flash-Showcase),
captured from the original SWFs running in Ruffle. Alt text carries no dates
(Otto, 27 Aug 2026: date-free presentation for this material).
"""
import base64, json, os, pathlib, urllib.request

REPO = pathlib.Path(__file__).resolve().parents[3]
for line in (REPO / '.env').read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

FOLDER = ('/Users/Ottinger/Documents/Oddtoe - iCloud Apple/'
          'Oddtoe (From US Computer - Need to Organise in 2014)/00_Oddtoe-Curated-Library/08_Flash-Showcase')
SITE = 'https://www.oddtoe.com'
auth = 'Basic ' + base64.b64encode(
    f"{os.environ['WP_ODDTOE_USER']}:{os.environ['WP_ODDTOE_APP_PASSWORD']}".encode()).decode()
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'

PLAN = [
    ('NGKids_Splash_FrontPage.gif',
     'National Geographic Kids homepage designed by Oddtoe: binocular navigation with Stories, Games, Sound Off and Try This sections',
     'NGK homepage — binocular navigation'),
    ('Immersive-Homepage.gif',
     'Animated immersive homepage feature for National Geographic Kids, layered underwater scene with welcome banner',
     'NGK immersive homepage feature (animated)'),
    ('BackTalk_PigFridge.gif',
     'Back Talk interactive for National Geographic Kids: a caption being typed into a thought balloon over a photo of a pig at a fridge',
     'Back Talk caption game (animated)'),
    ('WhatInTheWorld_Mantis.gif',
     'What in the World photo puzzle for National Geographic Kids: an anagram game revealing a praying mantis close-up',
     'What in the World? anagram puzzle (animated)'),
    ('WildWacky_MadLib_Payoff.png',
     'Wild and Wacky fill-in story for National Geographic Kids: the finished illustrated story after the reader fills fifteen blanks',
     'Wild & Wacky fill-in story — payoff screen'),
    ('GreenOMeter_Title.png',
     'Green-o-Meter eco quiz title screen for National Geographic Kids, cartoon kids in a rowboat',
     'Green-o-Meter eco quiz'),
    ('Brainteasers_Title.png',
     'Brainteasers quiz engine title screen for National Geographic Kids',
     'Brainteasers quiz engine'),
    ('NGDog.gif',
     'Animated dog character with a doghouse from a National Geographic Kids interactive',
     'NG dog character (animated)'),
]

out = {}
for fn, alt, title in PLAN:
    data = open(os.path.join(FOLDER, fn), 'rb').read()
    ctype = 'image/gif' if fn.endswith('.gif') else 'image/png'
    req = urllib.request.Request(SITE + '/wp-json/wp/v2/media', data=data, method='POST', headers={
        'Content-Type': ctype, 'Content-Disposition': f'attachment; filename="{fn}"',
        'Authorization': auth, 'User-Agent': UA})
    with urllib.request.urlopen(req) as r:
        d = json.load(r)
    mid = d['id']
    req2 = urllib.request.Request(SITE + f'/wp-json/wp/v2/media/{mid}',
        data=json.dumps({'alt_text': alt, 'title': title}).encode(), method='POST',
        headers={'Content-Type': 'application/json', 'Authorization': auth, 'User-Agent': UA})
    urllib.request.urlopen(req2).read()
    out[fn] = mid
    print('uploaded:', fn, '->', mid)
print(json.dumps(out))
