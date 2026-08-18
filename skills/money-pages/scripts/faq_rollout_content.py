"""Per-page Q&A content for the 18 Aug 2026 Oddtoe FAQ rollout.

Every answer is written only from facts already on the page it sits on.
No invented pricing, turnaround, deliverables, team size or client names.
Bold follows the design-kit rule: key entities and keyphrases only, 2-3 per
answer, plus the brand name. No new internal links — the link question was
never signed off, so answers stay plain text.
"""

def before_form(src):
    """Row that carries the Gravity Form — the FAQ goes immediately above it."""
    i = src.index('[gravityform')
    return src.rfind('[vc_row', 0, i)

def before_last_row(src):
    return src.rfind('[vc_row')


PAGES = [
  dict(slug='prop-designer-maker', id=13753, mode='append', tag='faqprop',
       new=[
    ('How do you hire a prop maker in Australia?',
     'Send the brief &mdash; what the prop is, when it is needed, and where it has to travel. <strong>Oddtoe</strong> is based in <strong>Melbourne</strong> and works with theatre companies, film and TV productions and event teams across <strong>Australia</strong>. Concept, design and fabrication can be taken together, or picked up at whichever stage you are stuck on.'),
    ('What is the difference between a prop designer and a prop maker?',
     'The <strong>prop designer</strong> works out what the prop should be and how it needs to read on camera or on stage. The <strong>prop maker</strong> builds it. <strong>Oddtoe</strong> does both, which removes the handover where a design quietly gets simplified into something cheaper to build.'),
    ('What kinds of props does Oddtoe make?',
     'Props and set pieces for <strong>film, TV, theatre and events</strong> &mdash; character props, oversized and sculptural pieces, and <strong>3D-designed builds</strong> that exist as a digital model before anything is cut. Design can be supplied on its own if you already have a fabricator.'),
       ]),

  dict(slug='weird-art', id=14629, mode='new_row', tag='faqweird',
       topic='Weird Art', anchor=before_form, vc_id='1787200000001',
       new=[
    ('What is weird art?',
     'Art that deliberately breaks the familiar &mdash; where <strong>geometric shapes</strong> take on lives of their own and become surreal character studies, and portraiture is blended with <strong>caricature</strong>. It is less a movement than an aesthetic, and at <strong>Oddtoe</strong> it is used mostly for <strong>visual humour</strong>.'),
    ('Where does weird art take its inspiration from?',
     'From everywhere &mdash; the organic forms found in nature, the sleek lines of <strong>industrial design</strong>, the exaggerated features of <strong>caricature</strong>, and the whimsy of sculpture. <strong>Oddtoe</strong> mixes those with <strong>illustration and character design</strong>.'),
    ('Has AI changed weird art?',
     'Yes, and partly by accident. <strong>AI digital art</strong> has added enormously to the body of weird art, and generative models still struggle with things like hands and feet &mdash; those failures have an aesthetic of their own. At <strong>Oddtoe</strong> the AI is directed rather than left to its own devices.'),
    ('Can weird art be used commercially?',
     'Yes. It suits a brand or an institution that would rather be remembered than agreeable &mdash; <strong>campaign imagery</strong>, <strong>character design</strong>, editorial illustration, and pieces people stop to photograph.'),
       ]),

  dict(slug='roboticist', id=11166, mode='new_row', tag='faqrobo',
       topic='Creative Robotics', anchor=before_form, vc_id='1787200000002',
       new=[
    ('What is a roboticist?',
     'A professional who specialises in designing, developing and operating robots, combining <strong>engineering</strong>, <strong>computer science</strong> and <strong>artificial intelligence</strong>. Roboticists build robots for everything from manufacturing and research to entertainment and public installations.'),
    ('What does a creative roboticist do?',
     'A <strong>creative roboticist</strong> works on how a robot looks, moves and reads to an audience, not only on whether it functions. <strong>Oddtoe</strong> designs and prototypes robots using kits and <strong>generative AI</strong>, which gets to a working prototype far faster than building every part from scratch.'),
    ('Who hires a creative roboticist?',
     '<strong>Tech companies, film productions, museums, start-ups, advertising agencies</strong> and futurists &mdash; usually when a robot has to be seen by an audience rather than just work on a factory floor.'),
    ('Is a roboticist the same as a robotics engineer?',
     'Not quite. A <strong>robotics engineer</strong> is usually focused on mechanics, electronics and control systems. <strong>Roboticist</strong> is the broader term and takes in design, behaviour and application as well. <strong>Oddtoe</strong> works on the design and prototyping side.'),
       ]),

  dict(slug='generative-ai-artist', id=13139, mode='new_row', tag='faqgenai',
       topic='Generative AI Art', anchor=before_form, vc_id='1787200000003',
       new=[
    ('What is a generative AI artist?',
     'An artist who directs <strong>generative AI</strong> as a tool inside their own practice rather than treating whatever it produces as finished. At <strong>Oddtoe</strong> that is a hybrid workflow &mdash; <strong>AI image generation, graphic design and digital illustration</strong> used together.'),
    ('What is a generative cartoonist?',
     'A cartoonist who uses generative AI for <strong>character work and visual gags</strong> while keeping the writing, the timing and the final choice of image with the artist. The machine supplies options; the cartoonist decides which one is funny.'),
    ('Why hire a professional AI artist instead of prompting it yourself?',
     'Consistency. Generative AI produces <strong>inconsistent illustrations</strong> &mdash; fine for a one-off, a real problem for a brand that needs a <strong>cohesive style</strong> across a campaign or a series. A professional supplies the <strong>art direction</strong> that holds the look together across dozens of images.'),
    ('What is Oddtoe&rsquo;s background as an artist?',
     'Illustration is the foundational skill, with a career that has taken in <strong>political cartooning, puppetry, data visualisation and street art</strong>. <strong>Oddtoe</strong> has worked since 2006 for organisations including <strong>National Geographic</strong>.'),
       ]),

  dict(slug='topiarist', id=11160, mode='append', tag='faqtopi',
       new=[
    ('What is a topiarist?',
     'A designer and gardener who shapes living plants into sculptural forms. A <strong>topiary artist</strong> works with hedging and shrubs the way a sculptor works with material, with the difference that the piece keeps growing after it is installed.'),
    ('Do you take on custom topiary design and fabrication?',
     'Yes. <strong>Oddtoe</strong> designs custom topiary for <strong>gardens, parks and public spaces</strong>, and can hand over the design as a <strong>3D render</strong> for a landscaper to plant and maintain, or work through fabrication where a frame is involved.'),
    ('Where does Oddtoe work as a topiarist?',
     '<strong>Melbourne</strong> and across <strong>Australia</strong>, on both <strong>private gardens and public commissions</strong>.'),
       ]),

  dict(slug='animation-conferences-2026-2027', id=13839, mode='new_row', tag='faqconf',
       topic='Animation Conferences', anchor=before_last_row, vc_id='1787200000004',
       bg='#0f111b',
       new=[
    ('When are most animation conferences held?',
     'They run right across the calendar year, but there are two clear clusters &mdash; <strong>April</strong> and <strong>October</strong> are consistently the heaviest months for animation festivals and conventions. <strong>Europe dominates</strong> the calendar.'),
    ('What is the difference between an animation conference, a festival and a trade show?',
     'A <strong>festival</strong> is built around screenings and awards. A <strong>conference</strong> is built around talks and panels. A <strong>trade show</strong> is built around exhibitors and business meetings. Several of the biggest events are all three at once, which is usually what makes the travel worth it.'),
    ('Are animation conferences worth attending virtually?',
     'Some are. The talks translate to a screen; the networking rarely does. If the reason for going is to meet <strong>animation agents</strong> or studio decision-makers, in person is worth the cost.'),
    ('How were the conferences on this list chosen?',
     'On two things: a great <strong>festival culture</strong> for attendees, and a genuine <strong>professional experience</strong> for animators, animation agents and industry people who want to meet the decision-makers rather than just watch shorts.'),
       ]),

  dict(slug='character-designer', id=13701, mode='append', tag='faqchar',
       new=[
    ('How do you hire a character designer?',
     'Send the brief &mdash; what the character is for, the medium it has to work in, and the style you are drawn to. <strong>Oddtoe</strong> takes <strong>character design</strong> for books, comics, games, animated series and films, either as a full commission or as a design pass over characters you already have.'),
    ('What does a character design service include?',
     'Usually concept sketches, a settled <strong>character sheet</strong>, and the artwork a production needs to work from. Exact deliverables and the number of revision rounds are agreed with the brief so nothing is open-ended.'),
    ('What makes a good character designer?',
     'Range, and judgement about which sketch is the one. A good <strong>character designer</strong> can push a face past realistic into something readable at a glance. <strong>Oddtoe</strong> leans to the over-the-top &mdash; villains, nerds, the overly vain, and characters with a bizarre way of looking at the world.'),
       ]),

  dict(slug='experiential-design-techniques-examples', id=11253, mode='post', type='posts',
       tag='faqexp',
       new=[
    ('What is experiential design?',
     'The design of a physical or immersive experience so that an audience remembers it and forms a positive association with a brand or a cultural institution. It combines spatial design, technology and storytelling, and it only works when the audience is understood first.'),
    ('What are examples of experiential design?',
     'Spatial augmented reality, video installations, interactive walls that generate real-time graphics from people&rsquo;s movement, and interactive music played with hand motions. The six techniques covered above are the ones Oddtoe expects to matter most.'),
    ('What is the difference between experiential design and event marketing?',
     'Event marketing is the whole campaign around an event &mdash; the audience, the promotion, the reason to turn up. Experiential design is the part people physically walk into and interact with. One brings them; the other is what they remember.'),
       ]),
]
