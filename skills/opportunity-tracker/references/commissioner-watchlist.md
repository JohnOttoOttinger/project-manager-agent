# Commissioner watchlist — Oddtoe

Built 1 September 2026 after the [open-call aggregator survey](opencall-aggregator-survey.md)
showed that aggregators are thin and gated for this practice. **These are not live
calls.** Each row is an organisation that commissions Oddtoe's kind of work, with a
URL that was machine-checked on 1 Sep 2026 and a note on when to look. They are in
the board as `kind = scouting` under `source_id` `commissioner-watchlist-2026-09-01`,
so the whole batch can be removed in one statement.

Deadlines are deliberately **empty**. A watchlist entry carrying a date nobody read
is the exact failure this stream exists to prevent — the date arrives when someone
opens the organiser's page.

## Act on these first

1. **Amsterdam Light Festival** — the Edition 16 (2027-28) open call opens **early
   September 2026**, i.e. now. The festival states plainly that newcomers as well as
   light-art professionals may submit, so one public credit is not disqualifying.
2. **Lorne Sculpture Biennale** — biennial in March; the 2025 edition ran 1-30 Mar,
   so the March 2027 artist call should open around **mid-2026**.
3. **Sculpture by the Sea, Bondi** — 2026 submissions closed 19 Apr 2026 and the show
   runs 16 Oct - 2 Nov 2026. Visit it as scouting, and diarise **February 2027**.
   Awards are the largest here: $70,000 acquisitive plus three Lempriere scholarships.
4. **International Garden Festival (Jardins de Métis)** and **Chaumont-sur-Loire** —
   both run genuine international open calls for *conceptual* gardens. This is the
   best match on the list for the topiary and sensory-garden strand.
5. **Melbourne International Flower & Garden Show** — juried show gardens, in Otto's
   own city, and essentially uncontested by anyone from the experiential field.

## Checking the list stays alive

`scripts/commissioner-watchlist/check_urls.py` re-probes every URL and reports which
resolved. On the first run 37 of 45 answered 200; five councils and Creative Victoria
return 403 to automated checks (a firewall, not a dead link), Sónar issues a 308, and
two — Lorne and Luminale — did not answer at all but were confirmed alive by hand.

## The list

### Art-tech / new media (9)

| Organisation | Where | Link |
| --- | --- | --- |
| ANAT (Australian Network for Art and Technology) | Adelaide, Australia | <https://www.anat.org.au/opportunities/> |
| Ars Electronica | Linz, Austria | <https://ars.electronica.art/prix/en/> |
| Athens Digital Arts Festival | Athens, Greece | <https://www.adaf.gr/> |
| Currents New Media | Santa Fe NM, United States | <https://currentsnewmedia.org/> |
| Dark Mofo | Hobart, Australia | <https://darkmofo.net.au/> |
| FILE Sao Paulo | Sao Paulo, Brazil | <https://file.org.br/> |
| ISEA (International Symposium on Electronic Art) | rotating, International | <https://www.isea-international.org/> |
| MUTEK | Montreal, Canada | <https://mutek.org/> |
| Sonar+D | Barcelona, Spain | <https://sonar.es/> |

### Council / agency (VIC) (8)

| Organisation | Where | Link |
| --- | --- | --- |
| City of Melbourne — public art | Melbourne, Australia | <https://www.melbourne.vic.gov.au/arts-and-culture> |
| City of Port Phillip — public art | Melbourne, Australia | <https://www.portphillip.vic.gov.au/> |
| City of Yarra — public art | Melbourne, Australia | <https://www.yarracity.vic.gov.au/> |
| Creative Victoria | Melbourne, Australia | <https://creative.vic.gov.au/> |
| Darebin City Council — arts | Melbourne, Australia | <https://www.darebin.vic.gov.au/> |
| Maribyrnong City Council — public art | Melbourne, Australia | <https://www.maribyrnong.vic.gov.au/> |
| Merri-bek City Council — public art | Melbourne, Australia | <https://www.merri-bek.vic.gov.au/> |
| Wyndham City Council — public art | Melbourne, Australia | <https://www.wyndham.vic.gov.au/services/arts-culture> |

### Garden / horticultural (7)

| Organisation | Where | Link |
| --- | --- | --- |
| Domaine de Chaumont-sur-Loire International Garden Festival | Chaumont-sur-Loire, France | <https://www.domaine-chaumont.fr/en_GB> |
| Floriade Canberra | Canberra, Australia | <https://floriadeaustralia.com/> |
| International Garden Festival (Jardins de Metis) | Grand-Metis, Quebec, Canada | <https://jardinsdemetis.com/> |
| Melbourne International Flower & Garden Show | Melbourne, Australia | <https://melbflowershow.com.au/> |
| RHS Chelsea Flower Show | London, United Kingdom | <https://www.rhs.org.uk/shows-events/rhs-chelsea-flower-show> |
| RHS Hampton Court Palace Garden Festival | London, United Kingdom | <https://www.rhs.org.uk/shows-events/rhs-hampton-court-palace-garden-festival> |
| Singapore Garden Festival | Singapore, Singapore | <https://www.nparks.gov.sg/> |

### Institution (3)

| Organisation | Where | Link |
| --- | --- | --- |
| ACMI | Melbourne, Australia | <https://www.acmi.net.au/> |
| Federation Square | Melbourne, Australia | <https://fedsquare.com/> |
| Regional Arts Victoria | Victoria, Australia | <https://www.rav.net.au/> |

### Light / projection festival (10)

| Organisation | Where | Link |
| --- | --- | --- |
| Amsterdam Light Festival | Amsterdam, Netherlands | <https://amsterdamlightfestival.com/en/open-call> |
| Bella Skyway Festival | Torun, Poland | <https://www.bellaskyway.pl/en/> |
| Fête des Lumières Lyon | Lyon, France | <https://www.fetedeslumieres.lyon.fr/en> |
| GLOW Eindhoven | Eindhoven, Netherlands | <https://gloweindhoven.nl/en/> |
| LUX Helsinki | Helsinki, Finland | <https://luxhelsinki.fi/en/> |
| Lumiere (Artichoke) | Durham / London, United Kingdom | <https://www.artichoke.uk.com/> |
| Luminale Frankfurt | Frankfurt, Germany | <https://luminale-frankfurt.de/> |
| Signal Festival Prague | Prague, Czechia | <https://www.signalfestival.com/> |
| Winter Lights Canary Wharf | London, United Kingdom | <https://canarywharf.com/whats-on/winter-lights/> |
| i Light Singapore | Singapore, Singapore | <https://www.ilightsingapore.gov.sg/> |

### Sculpture prize / trail (AU) (7)

| Organisation | Where | Link |
| --- | --- | --- |
| Lorne Sculpture Biennale | Lorne VIC, Australia | <https://lornesculpture.com/> |
| McClelland Sculpture Survey & Award | Langwarrin VIC, Australia | <https://mcclelland.org.au/> |
| Montalto Sculpture Prize | Red Hill VIC, Australia | <https://montalto.com.au/pages/sculpture> |
| Sculpture at Scenic World | Katoomba NSW, Australia | <https://www.scenicworld.com.au/> |
| Sculpture by the Sea | Sydney (Bondi) & Perth (Cottesloe), Australia | <https://sculpturebythesea.com/bondi/artists/> |
| Swell Sculpture Festival | Currumbin, Gold Coast, Australia | <https://www.swellsculpture.com.au/> |
| Woollahra Small Sculpture Prize | Sydney, Australia | <https://www.woollahra.nsw.gov.au/> |

### Sculpture prize / trail (INTL) (1)

| Organisation | Where | Link |
| --- | --- | --- |
| Yorkshire Sculpture Park | Wakefield, United Kingdom | <https://ysp.org.uk/> |
