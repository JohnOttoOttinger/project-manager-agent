import json,re,base64,urllib.parse,urllib.request,os,sys
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
auth=base64.b64encode(f"{os.environ['WP_ODDTOE_USER']}:{os.environ['WP_ODDTOE_APP_PASSWORD']}".encode()).decode()
H={'Authorization':'Basic '+auth,'User-Agent':UA,'Content-Type':'application/json'}
def get(i):
    return json.load(urllib.request.urlopen(urllib.request.Request(
        f'https://www.oddtoe.com/wp-json/wp/v2/pages/{i}?context=edit&_fields=content',headers=H)))['content']['raw']
def put(i,c):
    return json.load(urllib.request.urlopen(urllib.request.Request(
        f'https://www.oddtoe.com/wp-json/wp/v2/pages/{i}',data=json.dumps({'content':c}).encode(),
        method='POST',headers=H)))['content']['raw']==c
def link(anchor,url):
    return f'<strong><a class="dfd-custom-link-decorated" href="{url}">{anchor}</a></strong>'

# (page id, slug, [(exact text to find, anchor inside it, target url)])
PLAN=[
 (14629,'weird-art',[
   ('<strong>illustration and character design</strong>',
    '<strong><a class="dfd-custom-link-decorated" href="/artist-designer/character-designer/">illustration and character design</a></strong>'),
   ('<strong>geometric shapes</strong> take on lives of their own',
    '<strong><a class="dfd-custom-link-decorated" href="/geometric-art/">geometric shapes</a></strong> take on lives of their own'),
 ]),
 (13701,'character-designer',[
   ('characters with a bizarre way of looking at the world',
    'characters with '+link('a bizarre way of looking at the world','/weird-art/')),
   ('books, comics, games, animated series and films',
    'books, comics, games, '+link('animated series','/studio/original-stories/')+' and films'),
 ]),
 (13139,'generative-ai-artist',[
   ('<strong>Oddtoe</strong> has worked since 2006 for organisations',
    '<strong>Oddtoe</strong> has worked '+link('since 2006','/about-oddtoe/')+' for organisations'),
   ('<strong>character work and visual gags</strong>',
    '<strong><a class="dfd-custom-link-decorated" href="/artist-designer/character-designer/">character work</a> and visual gags</strong>'),
 ]),
 (13753,'prop-designer-maker',[
   ('<strong>3D-designed builds</strong> that exist as a digital model',
    '<strong><a class="dfd-custom-link-decorated" href="/portfolio-aggregate/">3D-designed builds</a></strong> that exist as a digital model'),
 ]),
 (11160,'topiarist',[
   ('as a <strong>3D render</strong> for a landscaper',
    'as a <strong><a class="dfd-custom-link-decorated" href="/portfolio-aggregate/">3D render</a></strong> for a landscaper'),
 ]),
 (11166,'roboticist',[
   ('start-ups, advertising agencies</strong> and futurists',
    'start-ups, <a class="dfd-custom-link-decorated" href="/experiential-marketing/">advertising agencies</a></strong> and futurists'),
 ]),
]

apply_ = '--apply' in sys.argv
for pid,slug,edits in PLAN:
    src=get(pid); out=src
    for old,new in edits:
        assert out.count(old)==1, f'{slug}: not unique/found -> {old[:60]!r}'
        out=out.replace(old,new,1)
    assert out.count('\r')==src.count('\r'), slug+': CRLF changed'
    added=out.count('dfd-custom-link-decorated')-src.count('dfd-custom-link-decorated')
    print(f"{slug:<24} +{added} link(s)  {len(src)} -> {len(out)} chars")
    if apply_:
        print(f"{'':<24} saved: {put(pid,out)}")
print('\napplied' if apply_ else '\ndry run — nothing written')
