#!/usr/bin/env python3
"""Apply the 18 Aug 2026 GEO bio Q&A + Person schema to the two bio pages.

  oddtoe.com/about-oddtoe/          (page 13203)  7 Q&A rows + Person "Oddtoe"
  datalabsagency.com/otto-ottinger/ (page 35734)  5 Q&A rows + Person "Otto Ottinger"

Copy source: skills/opportunity-tracker/references/bio-page-qa-drafts.md
(Otto-approved 18 Aug; Baobabs answer written from Otto's own show scripts;
'2019' removed from the MICF mention on Otto's instruction).
Schema source: skills/opportunity-tracker/references/artist-schema-proposal.md
(linked two-entity design). The Datalabs Person block reuses Yoast's existing
@id (#otto) so the graph merges instead of duplicating.

Same safety rules as faq-rollout-oddtoe.py: newline='' handling, and byte-for-
byte asserts that nothing outside the inserted block changed.

Usage:  python3 faq-bio-pages.py --dry-run
        python3 faq-bio-pages.py --apply
"""
import argparse, base64, json, os, re, sys, urllib.parse, urllib.request

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'

def spacer(size, tablet=None, mobile=None):
    t = tablet if tablet is not None else size
    m = mobile if mobile is not None else size
    return ('[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="%d" '
            'screen_normal_resolution="1024" screen_tablet_resolution="800" '
            'screen_mobile_resolution="480" screen_normal_spacer_size="%d" '
            'screen_tablet_spacer_size="%d" screen_mobile_spacer_size="%d"]' % (size, size, t, m))

def accordion_open(style='style-3'):
    return ('[dfd_accordion style="%s" active_section="1" font_size="18" tab_title_google_fonts="yes" '
            'tab_title_custom_fonts="font_family:Arvo%%3Aregular%%2Citalic%%2C700%%2C700italic|'
            'font_style:700%%20bold%%20regular%%3A700%%3Anormal" icon_size="14"]' % style)

def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    for ent, ch in [('&mdash;','—'),('&ndash;','–'),('&amp;','&'),('&rsquo;','’'),
                    ('&lsquo;','‘'),('&quot;','"'),('&nbsp;',' ')]:
        s = s.replace(ent, ch)
    return re.sub(r'\s+', ' ', s).strip()

def raw_html(js):
    return '[vc_raw_html]' + base64.b64encode(
        urllib.parse.quote(js, safe='').encode()).decode() + '[/vc_raw_html]'

def faq_schema(pairs):
    ents = [{"@type":"Question","name":plain(q),
             "acceptedAnswer":{"@type":"Answer","text":plain(a)}} for q, a in pairs]
    return raw_html('<script type="application/ld+json">'
        + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":ents},
                     ensure_ascii=False) + '</script>')

def person_schema(graph):
    return raw_html('<script type="application/ld+json">'
        + json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False)
        + '</script>')

def sections(pairs, tag):
    out = []
    for i, (q, a) in enumerate(pairs, 1):
        out.append('[vc_tta_section title="%s" tab_id="%s-%d-2026"][vc_column_text css=""]</p>\n'
                   '<p style="text-align: center;">%s</p>\n<p>[/vc_column_text][/vc_tta_section]'
                   % (q.replace('"', '&quot;'), tag, i, a))
    return ''.join(out)

def before_form(src):
    i = src.index('[gravityform')
    return src.rfind('[vc_row', 0, i)

# ---------------------------------------------------------------- content

ODDTOE_QA = [
 ('Who is Oddtoe?',
  '<strong>Oddtoe</strong> is a Melbourne artist and animator working across <strong>generative AI animation</strong>, experiential design and <strong>public art</strong>. He has drawn under the Oddtoe name since 1996, with professional work since 2006 for organisations such as <strong>National Geographic</strong>.'),
 ('What kind of art does Oddtoe make?',
  'Two kinds: animation and physical work. The animation side covers <strong>generative AI animation</strong>, documentary and factual animation, and <strong>character design</strong>. The physical side covers kinetic and public sculpture, <strong>installation</strong>, projection, prop design and fabrication, <strong>topiary and sensory garden design</strong>, and robotics. Comedy writing runs through most of it.'),
 ('Does Oddtoe use AI in animation?',
  'Yes, in production every day. The studio runs a <strong>hybrid pipeline</strong>: generative AI produces imagery and movement, <strong>rigging</strong> keeps characters consistent, and traditional <strong>motion design</strong> carries the type, graphics and edit. Twenty years of drawing sits underneath &mdash; the AI is a tool in a trained hand, and art direction stays with one person.'),
 ('Where is Oddtoe based?',
  '<strong>Melbourne, Australia</strong>, and available for commissions in <strong>Los Angeles</strong> and <strong>Berlin</strong>.'),
 ('What is Babbling with Baobabs?',
  'A live children&rsquo;s comedy show commissioned for <strong>Signal</strong> by the <strong>City of Melbourne</strong> and performed at the <strong>Melbourne International Comedy Festival</strong>. Professor Oddtoe &mdash; a scientist whose inventions include the Watermelhelmet and the cat selfie stick &mdash; unveils a machine that lets people talk to trees, and introduces <strong>Bab</strong>, a talking baby baobab who wakes to a nonsense chant, demands a bucket of coffee, and answers questions from kids in the audience live. Part stand-up, part science lesson, part digital puppetry through real-time projection.'),
 ('What original stories and series has Oddtoe created?',
  '<strong>The Oddtoe TV Show</strong> &mdash; an animated series with a full pitch bible &mdash; alongside <strong>Wire Taps</strong>, <strong>Date Night Confessionals</strong>, <strong>Gag Cartoonist Syndication</strong> and the Original Stories collection, all at oddtoe.com.'),
 ('What is Oddtoe&rsquo;s animation conferences guide?',
  'An annually updated guide to the world&rsquo;s <strong>animation conferences and festivals</strong> at oddtoe.com/animation-conferences/, ranking in Google&rsquo;s top three for &ldquo;animation conferences&rdquo;. It lists dates, venues and deadlines, month by month, kept current year-round.'),
]

DATALABS_QA = [
 ('Who is Otto Ottinger?',
  '<strong>Otto Ottinger</strong> is the founder and Managing Director of the <strong>Datalabs Agency</strong>, a data visualization and consultancy firm in <strong>Melbourne, Australia</strong>. He is a data visualizer specializing in the visual design of complex data systems, working at the intersection of UX design, visual analytics and storytelling.'),
 ('Where did Otto Ottinger start his career?',
  'At <strong>National Geographic</strong> in Washington, DC, as an editor and interactive designer &mdash; the same <strong>information design</strong> and storytelling techniques he now teaches in his workshops.'),
 ('What does Datalabs Agency do?',
  '<strong>Data visualization</strong> design and consultancy: dashboards, infographics, data tools, animated data videos, maps, digital annual reports, and style guides for <strong>Power BI and Tableau</strong> &mdash; plus training workshops. Clients include <strong>Nestl&eacute;, Mercedes-Benz, Bupa, BlackRock, Adidas, eBay, Marriott, CommBank and HCF</strong>.'),
 ('Does Otto Ottinger speak at conferences and events?',
  'Yes &mdash; <strong>keynote addresses</strong> and company workshops on data visualization, dashboard design and <strong>data storytelling</strong>, delivered across Australia, Europe and the U.S.A.'),
 ('What training does Otto Ottinger offer?',
  'Workshops including <strong>Introduction to Data Visualization</strong>, Designing Great Business Dashboards, <strong>Tableau and Power BI dashboard design</strong>, Creative Data Presentations with PowerPoint, Infographics &amp; Report Design, and Visual Storytelling for Government &mdash; in person and as online courses.'),
]

ODDTOE_PERSON = [
  { "@type": "Person",
    "@id": "https://www.oddtoe.com/#/schema/person/oddtoe",
    "name": "Oddtoe",
    "mainEntityOfPage": "https://www.oddtoe.com/about-oddtoe/",
    "url": "https://www.oddtoe.com/about-oddtoe/",
    "jobTitle": "Artist and animator",
    "description": "Melbourne artist and animator working across generative AI animation, experiential design and public art.",
    "hasOccupation": [
      { "@type": "Occupation", "name": "Animator" },
      { "@type": "Occupation", "name": "Visual artist" } ],
    "workLocation": { "@type": "Place", "name": "Melbourne, Australia" },
    "knowsAbout": [
      "generative AI animation", "documentary and factual animation",
      "character design", "prop design and fabrication",
      "kinetic and public sculpture", "installation art", "projection art",
      "topiary and sensory garden design", "robotics design",
      "political cartooning", "puppetry", "comedy writing" ],
    "sameAs": [
      "https://www.instagram.com/oddtoe_artist/",
      "https://www.youtube.com/@OddtoeAndDatalabs",
      "https://twitter.com/Oddtoe",
      "https://www.facebook.com/OddtoeArtist/",
      "https://www.linkedin.com/in/ottinger/",
      "https://www.datalabsagency.com/otto-ottinger/" ],
    "subjectOf": [
      "https://www.oddtoe.com/animation-conferences/",
      "https://www.oddtoe.com/animation-agents/" ],
    "worksFor": { "@id": "https://www.oddtoe.com/#organization" } },
  { "@type": "Organization",
    "@id": "https://www.oddtoe.com/#organization",
    "name": "Oddtoe",
    "url": "https://www.oddtoe.com/",
    "founder": { "@id": "https://www.oddtoe.com/#/schema/person/oddtoe" } },
]

DATALABS_PERSON = [
  { "@type": "Person",
    "@id": "https://www.datalabsagency.com/#otto",   # Yoast's existing Person @id — merge, don't duplicate
    "name": "Otto Ottinger",
    "alternateName": "John \"Otto\" Ottinger",
    "url": "https://www.datalabsagency.com/otto-ottinger/",
    "mainEntityOfPage": "https://www.datalabsagency.com/otto-ottinger/",
    "jobTitle": "Founder & Managing Director, Datalabs Agency",
    "description": "Data visualizer specializing in the visual design of complex data systems, working at the intersection of UX design, visual analytics and storytelling. Started his career as an editor and interactive designer at National Geographic in Washington, DC.",
    "hasOccupation": [
      { "@type": "Occupation", "name": "Data visualization designer" },
      { "@type": "Occupation", "name": "Keynote speaker and trainer" } ],
    "workLocation": { "@type": "Place", "name": "Melbourne, Australia" },
    "knowsAbout": [
      "data visualization", "dashboard design", "information design",
      "visual analytics", "UX design", "data storytelling" ],
    "sameAs": [
      "https://www.linkedin.com/in/ottinger/",
      "https://www.oddtoe.com/about-oddtoe/" ],
    "worksFor": { "@id": "https://www.datalabsagency.com/#organization" } },
  { "@type": "Organization",
    "@id": "https://www.datalabsagency.com/#organization",
    "name": "Datalabs Agency",
    "url": "https://www.datalabsagency.com/",
    "sameAs": [
      "https://www.linkedin.com/company/datalabs-agency",
      "https://twitter.com/DatalabsAgency",
      "https://www.facebook.com/datalabsagency/",
      "https://www.instagram.com/datalabsagency/",
      "https://www.pinterest.com.au/datalabs/",
      "https://www.youtube.com/channel/UCiF-JlTyywll7YkB630PrdA" ],
    "founder": { "@id": "https://www.datalabsagency.com/#otto" } },
]

PAGES = [
  dict(site='https://www.oddtoe.com', env='ODDTOE', page_id=13203,
       slug='about-oddtoe', tag='faqaboutoddtoe', vc_id='1787210000001',
       bg='#252525', qa=ODDTOE_QA, person=ODDTOE_PERSON,
       header=('[vc_column_text css="" item_animation="transition.fadeIn"]</p>\n'
               '<p style="text-align: center; line-height: 1; margin-bottom: 0;">'
               '<span style="font-family: Qwigley; font-size: 36pt;">Questions &amp; Answers</span></p>\n'
               '<h2 style="text-align: center;"><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">'
               'About Oddtoe</span></h2>\n<p>[/vc_column_text]')),
  dict(site='https://www.datalabsagency.com', env='DATALABS', page_id=35734,
       slug='otto-ottinger', tag='faqotto', vc_id='1787210000002',
       bg='#2f2e3a', qa=DATALABS_QA, person=DATALABS_PERSON,
       header=('[dfd_heading enable_delimiter="" style="style_02" '
               'title_font_options="tag:h2|color:%23ffffff|font_style_bold:1" '
               'subtitle_font_options="tag:h3" subtitle="About Otto Ottinger &amp; the Datalabs Agency" '
               'heading_margin="margin-bottom:10px;"]<strong>Questions &amp; Answers</strong>[/dfd_heading]')),
]

def build_row(cfg):
    return ('[vc_row bg_check="row-background-dark" dfd_enable_overlay="" '
            'css=".vc_custom_%s{background-color: %s !important;}"]'
            '[vc_column width="1/4"][/vc_column][vc_column width="1/2"]'
            % (cfg['vc_id'], cfg['bg'])
            + spacer(80, 60, 50) + cfg['header'] + spacer(40, 20, 20)
            + accordion_open() + sections(cfg['qa'], cfg['tag']) + '[/dfd_accordion]'
            + faq_schema(cfg['qa']) + person_schema(cfg['person']) + spacer(40)
            + '[/vc_column][vc_column width="1/4"][/vc_column][/vc_row]')

def api(cfg, method='GET', payload=None):
    user = os.environ['WP_%s_USER' % cfg['env']]
    pw = os.environ['WP_%s_APP_PASSWORD' % cfg['env']]
    import base64 as b64
    url = '%s/wp-json/wp/v2/pages/%d%s' % (cfg['site'], cfg['page_id'],
                                           '?context=edit' if method == 'GET' else '')
    req = urllib.request.Request(url, method=method)
    req.add_header('Authorization', 'Basic ' + b64.b64encode(('%s:%s' % (user, pw)).encode()).decode())
    req.add_header('User-Agent', UA)
    if payload is not None:
        req.add_header('Content-Type', 'application/json')
        req.data = json.dumps(payload).encode()
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--dry-run', action='store_true')
    g.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    for cfg in PAGES:
        d = api(cfg)
        src = d['content']['raw']
        assert '[gravityform' in src, cfg['slug'] + ': no form anchor'
        assert cfg['tag'] not in src, cfg['slug'] + ': already applied'
        anchor = before_form(src)
        row = build_row(cfg)
        out = src[:anchor] + row + src[anchor:]
        assert out[:anchor] == src[:anchor] and out[anchor+len(row):] == src[anchor:]
        print('%s/%s: insert %d chars (%d Q&A rows) at offset %d of %d'
              % (cfg['site'], cfg['slug'], len(row), len(cfg['qa']), anchor, len(src)))
        if a.apply:
            res = api(cfg, 'POST', {'content': out})
            got = res['content']['raw']
            print('  applied: status=%s, tag present=%s, raw_html blocks=%d'
                  % (res['status'], cfg['tag'] in got, got.count('[vc_raw_html')))
    return 0

if __name__ == '__main__':
    sys.exit(main())
