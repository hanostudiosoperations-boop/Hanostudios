#!/usr/bin/env python3
"""Generate the service pages under services/.

These exist for search and for AI answer engines: the landing page is a
portfolio, and a portfolio does not answer "what does a Web3 motion design
agency actually do". Each page targets one service in plain prose, states the
real proof numbers, and carries Service + FAQPage schema.

Everything outside <main class="svc"> is taken verbatim from work/kalshi.html
so the five case studies and three service pages can never drift apart — the
menu, Calendly modal, CTA and footer are one source. Re-run after editing that
file's shell:

    python3 tools/make-service-pages.py

Copy rule: every number here must be true and must also appear in the visible
text, not only in schema. Schema that outruns the page is a manual action
waiting to happen.
"""

import json
import os
import re

BASE = "https://www.hanostudios.xyz"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORG = BASE + "/#organization"

# Proof points, stated once so every page agrees.
PROOF = {
    "followers": "148,000",
    "views": "30M+",
    "viral": "8,000,000",
    "crypteum": "34,000",
}


def shell():
    """Head + tail lifted from the Kalshi case study."""
    src = open(os.path.join(ROOT, "work", "kalshi.html")).read()
    head = src.split("<!-- ============ CASE STUDY ============ -->")[0]
    tail = src.split("</article>")[1]
    return head, tail


SERVICES = [
    dict(
        slug="web3-motion-design",
        nav="Web3 motion design",
        title="Web3 Motion Design Agency | Hano Studios",
        h1="Web3 motion design that makes complex products obvious",
        desc=("Web3 motion design agency for crypto, trading and fintech brands. "
              "We animated campaigns for Bybit EU and built a 148K-follower crypto "
              "channel on the same craft."),
        kicker="Service",
        lead=("We are a motion design agency built for Web3. Charts, tokenomics, "
              "order books and protocol mechanics are the hardest things in "
              "marketing to explain, and they are what we animate every day."),
        keywords=["Web3 motion design", "crypto motion graphics", "motion design agency",
                  "3D animation", "explainer video", "token animation"],
        sections=[
            ("What Web3 motion design actually is",
             ["Motion design in Web3 is not decoration on top of a deck. It is the "
              "translation layer between a technical product and an audience that "
              "will give you about three seconds before scrolling.",
              "A protocol, an exchange or a token has mechanics that are genuinely "
              "hard to explain in writing. Animation lets you show a value flow, a "
              "chart moving, a transaction settling, a yield curve bending. Done "
              "properly, a viewer who has never traded understands the product, and "
              "a viewer who trades daily does not feel talked down to.",
              "That dual audience is the entire difficulty, and it is the thing most "
              "generalist studios get wrong. They make something beautiful that says "
              "nothing, or something accurate that nobody watches."]),
            ("What we produce",
             ["Short-form vertical video for Instagram, TikTok and YouTube Shorts. "
              "Paid ad creative in every ratio a platform will take. Product and "
              "protocol explainers. Brand films. Data visualisation and chart "
              "animation. UI animation that walks a first-time user through an app "
              "before they download it.",
              "Every concept is adapted into the formats each placement needs, so one "
              "idea becomes a full matrix of deliverables in a single visual language."]),
            ("Proof this works",
             ["We built Hano Crypto, our own brand, from zero to %s followers and %s "
              "views on Instagram with over 200 videos, entirely organically. One "
              "video reached %s views and brought in more than 50,000 followers on "
              "its own." % (PROOF["followers"], PROOF["views"], PROOF["viral"]),
              "For Bybit EU we produced the visual campaign for their Bybit Stockholm "
              "Open tennis title sponsorship and the Europe-wide Bybit Card campaign, "
              "in English and Swedish, sized for every placement.",
              "The same system took The Crypteum from 400 followers to %s in three "
              "months." % PROOF["crypteum"]]),
            ("How we work",
             ["Direction is agreed before production starts, which is where expensive "
              "changes get caught. Every project includes two rounds of revisions at "
              "each stage. Single deliverables usually land in one to two weeks; "
              "retainers run on a fixed weekly cadence so you always know what is "
              "arriving and when."]),
        ],
        faqs=[
            ("What is a Web3 motion design agency?",
             "A studio that produces animation and video specifically for crypto, "
             "trading and fintech products. The difference from a general motion "
             "studio is domain knowledge: understanding what a perpetual, a bridge or "
             "an order book actually is, so the animation is accurate as well as "
             "attractive."),
            ("How much does Web3 motion design cost?",
             "It depends on scope, length and how many formats you need. We quote each "
             "project individually rather than publishing a rate card, because a "
             "single explainer and an ongoing content retainer are very different "
             "commitments. A short call gets you an accurate number."),
            ("How long does a motion design project take?",
             "Most single deliverables are finished within one to two weeks. Larger "
             "campaigns with multiple concepts and format adaptations run longer, and "
             "ongoing retainers deliver on a fixed weekly schedule agreed up front."),
            ("Do you work with brands outside crypto?",
             "Yes. Our focus is Web3, trading and fintech because that is where our "
             "domain knowledge compounds, but the craft transfers to any product with "
             "something complicated to explain."),
        ],
    ),
    dict(
        slug="crypto-social-media-management",
        nav="Crypto social media management",
        title="Crypto & Web3 Social Media Management Agency | Hano Studios",
        h1="Web3 social media management, run by people who grew their own audience",
        desc=("Crypto social media management agency. We grew Hano Crypto to 148,000 "
              "followers and 30M+ views organically, and run content for Kalshi, a "
              "$22B regulated exchange."),
        kicker="Service",
        lead=("Most agencies managing crypto social accounts have never grown one. We "
              "built a 148,000-follower channel from zero with no ads and no "
              "giveaways, and we run the same system for clients."),
        keywords=["crypto social media management", "Web3 social media agency",
                  "Instagram growth", "community growth", "content strategy",
                  "short-form video"],
        sections=[
            ("The problem with most crypto social content",
             ["Crypto content on social media collapses into two piles: price "
              "speculation and unsupported hype. Charts with bold predictions, or "
              "tokens pumped with no context and no value to the viewer.",
              "Both attract a narrow audience of people who already trade and already "
              "have opinions, and repel everyone else. That is a ceiling, and most "
              "accounts hit it within a few thousand followers."]),
            ("What we do instead",
             ["We treat each post as a story with a reason to watch to the end. Topic "
              "selection comes from daily research across price action, narrative "
              "shifts, regulatory news and on-chain data, scored on two axes: will "
              "this travel, and does it teach the viewer something.",
              "Scripting follows a five-step structure refined across more than 200 "
              "videos. Retention is engineered deliberately, with re-hooks placed "
              "through the video so watch time holds to the end. Watch time, not raw "
              "views, is what the algorithm actually rewards."]),
            ("Proof this works",
             ["Hano Crypto went from zero to %s followers and %s views, 100%% "
              "organically. No paid ads, no giveaway campaigns, no influencer "
              "partnerships. The most viral video reached %s views with an average "
              "watch time near a full minute."
              % (PROOF["followers"], PROOF["views"], PROOF["viral"]),
              "Kalshi, a CFTC-regulated exchange at a $22 billion valuation, made us "
              "their partner for crypto video content, published through that "
              "audience so their brand-new account did not have to start from zero.",
              "The Crypteum went from 400 followers to %s in three months, an 85x "
              "increase, with one video approaching a million views."
              % PROOF["crypteum"]]),
            ("What a retainer includes",
             ["Content strategy and topic research, scripting, production, editing and "
              "publishing. Instagram, TikTok, X, YouTube and LinkedIn as standard, "
              "each in the right ratio and length. Most relationships run monthly, "
              "with us functioning as the embedded content team rather than a vendor "
              "you brief and chase."]),
        ],
        faqs=[
            ("What does a crypto social media agency do?",
             "Strategy, content production and publishing for crypto and Web3 brands "
             "across short-form video platforms. The valuable part is not scheduling "
             "posts, it is knowing which topics will travel in this market and how to "
             "frame them so both newcomers and experienced traders keep watching."),
            ("Can you grow a brand-new account with no followers?",
             "Yes, and we have done it twice from zero. Hano Crypto reached 148,000 "
             "followers organically, and The Crypteum went from 400 to 34,000 in three "
             "months. A new account has no algorithmic trust, so the early work is "
             "engineering watch time rather than chasing follower counts."),
            ("Do you buy followers or run giveaways?",
             "No. Every number on this site is organic. Bought audiences do not "
             "engage, which means the algorithm stops distributing your content, and "
             "giveaway followers leave the moment the giveaway ends."),
            ("Which platforms do you manage?",
             "Instagram, TikTok, X, YouTube and LinkedIn as standard. Instagram and "
             "TikTok short-form video is where most of our results have come from."),
            ("How long before we see results?",
             "Retention improvements show within a few weeks, follower growth "
             "compounds over months. The Crypteum's 85x growth took a full quarter. "
             "Anyone promising a viral hit on a schedule is guessing."),
        ],
    ),
    dict(
        slug="web3-ad-campaigns",
        nav="Web3 ad campaigns",
        title="Web3 & Crypto Ad Campaign Agency | Hano Studios",
        h1="Ad campaigns for crypto brands, built to hold up at global scale",
        desc=("Web3 ad campaign agency. We produced two campaigns for Bybit EU, the "
              "world's second-largest crypto exchange, across two languages and every "
              "major placement."),
        kicker="Service",
        lead=("We concept, produce and adapt ad campaigns for crypto, trading and "
              "fintech brands, from a single hero film to a full matrix of "
              "platform-native cuts."),
        keywords=["Web3 ad campaign", "crypto advertising", "ad creative",
                  "campaign production", "paid social creative", "brand film"],
        sections=[
            ("What makes crypto advertising different",
             ["A crypto ad has to clear two bars at once. It has to be trustworthy "
              "enough for a regulated financial product, and interesting enough to "
              "survive a feed built for entertainment.",
              "Push too hard on polish and it reads as a bank advert nobody watches. "
              "Push too hard on hype and it reads as a scam, which in this category is "
              "fatal. The work sits in a narrow band between the two, and finding that "
              "band takes knowing the market."]),
            ("What we produce",
             ["Campaign concepting, scripting and storyboarding. Animation and 3D. "
              "Live-action integration and post. Localisation into other languages. "
              "Format adaptation so one concept runs cleanly on every placement it "
              "touches, from a 9:16 Reel to a landscape pre-roll.",
              "The point is one idea, one visual language, executed consistently "
              "everywhere, rather than a hero film and a set of afterthought crops."]),
            ("Proof this works",
             ["Bybit EU brought us in for two campaigns. The first was the visual "
              "campaign for their title sponsorship of the Stockholm Open, a three-year "
              "ATP tournament partnership running from 2026 through 2028, in front of "
              "roughly 30,000 spectators and a worldwide broadcast audience.",
              "The second was the Europe-wide campaign for the Bybit Card, a product "
              "with more than three million cardholders. Every concept was animated "
              "and adapted into four formats for all major platforms, produced in "
              "English and Swedish for the Nordic launch.",
              "Bybit has more than 80 million users and is the second-largest crypto "
              "exchange by volume. Work at that scale does not get signed off unless "
              "it is right."]),
            ("How a campaign runs",
             ["We agree direction before production starts, then concept, produce and "
              "adapt. Two rounds of revisions at each stage are included. Timelines "
              "depend on scope, but most campaigns move considerably faster than a "
              "traditional agency because strategy, design and animation sit in the "
              "same team rather than being handed between departments."]),
        ],
        faqs=[
            ("What does a Web3 ad campaign cost?",
             "It depends on concept count, production complexity and how many formats "
             "and languages you need. We quote per project. A single animated concept "
             "adapted to four placements and a multi-market campaign are very "
             "different budgets."),
            ("Do you handle strategy or just production?",
             "Both. Strategy, concept, copy, design, motion and distribution. "
             "Animation is one step in a system, not the product itself, and campaigns "
             "briefed as production-only usually underperform because the idea was "
             "settled before anyone thought about placement."),
            ("Can you produce in multiple languages?",
             "Yes. The Bybit Card campaign ran in English and Swedish for the Nordic "
             "launch, with every format adapted rather than subtitled."),
            ("Do you deliver paid social creative as well as brand films?",
             "Yes, and usually together. A brand film sets the visual language and the "
             "paid cuts carry it into the feed, which is what makes a campaign "
             "recognisable rather than a set of unrelated assets."),
        ],
    ),
    dict(
        slug="explainer-videos",
        nav="Explainer &amp; launch videos",
        title="Crypto & Web3 Explainer Video Agency | Hano Studios",
        h1="Explainer and launch videos for products people find hard to understand",
        desc=("Web3 explainer video agency. We animate protocols, exchanges and token "
              "mechanics so newcomers understand them and experienced traders still "
              "take them seriously."),
        kicker="Service",
        lead=("An explainer earns its budget when a stranger watches it and decides "
              "your product makes sense. That is a harder test than looking good, and "
              "it is the one we build for."),
        keywords=["explainer video", "crypto explainer video", "launch video",
                  "product video", "animated explainer", "protocol explainer"],
        sections=[
            ("What an explainer video has to do",
             ["Most explainers fail in the first five seconds, not the last thirty. "
              "They open by introducing the company instead of the problem, and the "
              "viewer leaves before the useful part arrives.",
              "In Web3 the difficulty doubles, because the audience splits. Half have "
              "never used a wallet; half trade daily and will close the tab the moment "
              "something is inaccurate. A good explainer serves both without patronising "
              "either, which means the script matters more than the render."]),
            ("Launch videos",
             ["A launch video is a different job from an explainer. It is not teaching, "
              "it is creating a reason to pay attention on a specific day.",
              "Those work when they are built around one clear idea and cut for the "
              "platform they will actually run on, rather than a two-minute film "
              "trimmed down afterwards. We produce the hero cut and the platform-native "
              "versions together, so the launch lands everywhere at once."]),
            ("What we produce",
             ["Product and protocol explainers. Launch and announcement films. App and "
              "UI walkthroughs that show a first-time user exactly what happens when "
              "they tap. 3D product animation. Data and chart visualisation. Scripts, "
              "storyboards, voiceover direction and sound design as part of the work, "
              "not as extras."]),
            ("Proof this works",
             ["Our own channel is the clearest evidence: %s videos explaining crypto "
              "topics to a mixed audience, %s followers and %s views, all organic. The "
              "most viral reached %s views with an average watch time near a full "
              "minute — on educational content, not a stunt."
              % ("200+", PROOF["followers"], PROOF["views"], PROOF["viral"]),
              "For Bybit EU we animated the Bybit Card as the hero of every frame "
              "across a Europe-wide campaign, and built UI animation of the Bybit app "
              "so a new user understands the product before downloading it."]),
        ],
        faqs=[
            ("How much does an explainer video cost?",
             "It depends on length, animation complexity and how many cuts you need. A "
             "single 60-second animated explainer and a launch package with platform "
             "variants are different budgets, so we quote per project after a short "
             "call about scope."),
            ("How long should an explainer video be?",
             "Long enough to be understood and no longer. For social placement, 45 to "
             "75 seconds is usually right; our own one-minute format outperformed the "
             "15-second content that dominated when we started, because watch time "
             "matters more to the algorithm than view count."),
            ("Do you write the script?",
             "Yes. Scripting is where an explainer is won or lost, so it is part of the "
             "work rather than something we ask you to supply. You review and approve "
             "direction before any animation starts."),
            ("Can you explain a technical protocol accurately?",
             "That is the specific thing we are built for. We work in crypto and "
             "trading every day, so the conversation starts at mechanics rather than "
             "definitions, and the output survives scrutiny from people who know the "
             "space."),
        ],
    ),
    dict(
        slug="web3-graphic-design",
        nav="Web3 graphic design &amp; brand identity",
        title="Web3 Graphic Design & Crypto Brand Identity | Hano Studios",
        h1="Graphic design and brand identity for crypto and Web3",
        desc=("Web3 graphic design agency. Brand identity, visual systems and campaign "
              "design for crypto, trading and fintech — built to be recognisable in a "
              "feed, not just in a brand book."),
        kicker="Service",
        lead=("A crypto brand is judged in a feed, at speed, next to competitors. We "
              "design identities that stay recognisable there, and the systems that "
              "keep them consistent across everything you ship."),
        keywords=["Web3 graphic design", "crypto brand identity", "visual identity",
                  "brand system", "campaign design", "social media design"],
        sections=[
            ("Identity that survives contact with a feed",
             ["Most brand guidelines are written for a website and a business card. In "
              "Web3 the primary surface is a 9:16 video on a phone, seen for a second "
              "and a half while someone scrolls.",
              "That changes what an identity needs to be. Colour has to hold at "
              "thumbnail size, type has to read at speed, and the system has to survive "
              "being animated. We design for that surface first and let the static "
              "applications follow."]),
            ("What we design",
             ["Full visual identity: logo, type system, colour, iconography and motion "
              "principles. Campaign design and key visuals. Social templates and "
              "thumbnail systems. Presentation and pitch design. Data and chart design "
              "systems for products where numbers are the story."]),
            ("Why the system matters more than the logo",
             ["Recognition compounds. A viewer scrolling their explore feed should be "
              "able to identify your brand before reading the account name, and that "
              "only happens when every asset follows the same rules.",
              "We build the rules and the components together, so consistency does not "
              "depend on someone remembering the guidelines every time."]),
            ("Proof this works",
             ["We built The Crypteum's entire visual identity from the ground up: a "
              "deliberate black-and-silver film language, high contrast and restrained, "
              "with every video playing as a sequence of designed frames rather than "
              "text over a static post. That account went from 400 followers to %s in "
              "three months." % PROOF["crypteum"],
              "Hano Crypto's own system uses a low-key palette with purple as the "
              "single accent, chosen because it reads as credible rather than "
              "speculative in a category full of red and green. It is now one of the "
              "most copied looks in crypto content on Instagram."]),
        ],
        faqs=[
            ("What does Web3 graphic design include?",
             "Visual identity, campaign design, social and thumbnail systems, "
             "presentation design and data visualisation. The Web3-specific part is "
             "designing for short-form video and feed placement first, because that is "
             "where crypto brands are actually seen."),
            ("Do you do full brand identity or only individual assets?",
             "Both. We have built identities from nothing, including The Crypteum's, "
             "and we also work inside existing brand systems where a client already has "
             "one they are happy with."),
            ("How is this different from a general design studio?",
             "Domain knowledge and format. We know what a chart, an order book or a "
             "tokenomics diagram needs to communicate, and we design assuming the work "
             "will be animated and watched on a phone rather than printed."),
            ("Do you deliver source files and guidelines?",
             "Yes. You get the working files and a system your team can apply without "
             "us, which is the point of a system rather than a set of one-off assets."),
        ],
    ),
    dict(
        slug="web3-website-design-development",
        nav="Web3 website design &amp; development",
        title="Web3 Website Design & Development | Hano Studios",
        h1="Web3 websites, designed and built",
        desc=("Web3 website design and development. We design and ship fast, "
              "motion-led sites for crypto, trading and fintech brands — design "
              "through launch, not a handoff."),
        kicker="Service",
        lead=("We design and build the site, rather than designing it and handing you "
              "a file. What you approve is what goes live, at the speed it was "
              "designed to run."),
        keywords=["Web3 website design", "crypto website development",
                  "website development", "landing page", "web design agency"],
        sections=[
            ("Design and build, one team",
             ["The usual failure in agency web work is the handoff. A studio designs "
              "something beautiful, a separate developer builds an approximation, and "
              "the motion that made the design work is the first thing dropped.",
              "We do both, so what gets approved is what ships. Animation is planned as "
              "part of the design rather than requested afterwards, which is why it "
              "survives to production and still performs."]),
            ("What we build",
             ["Brand and product sites. Campaign and launch landing pages. Documentation "
              "and content sites. Motion-led experiences where scroll and transition "
              "carry the story. Integrations with the tools you already run: analytics, "
              "booking, CRM, CMS and email.",
              "Note on scope: we design and build front-end experiences. We do not write "
              "or audit smart contracts, and we will say so rather than take work we "
              "should not."]),
            ("Fast by construction",
             ["A crypto audience arrives on mobile, often on a poor connection, and "
              "leaves if the page stalls. Performance is a design constraint from the "
              "start, not an optimisation pass at the end.",
              "That means restraint about what loads, media encoded properly, and "
              "animation that degrades gracefully when a script fails or a visitor "
              "prefers reduced motion — this site does exactly that, and stays fully "
              "readable with its animation library blocked."]),
            ("Proof this works",
             ["The site you are reading is ours: a static, no-framework build with "
              "scroll-driven animation, video case studies, structured data and a "
              "booking flow, and it stays usable if the animation library never loads.",
              "The same team produces the motion work behind Bybit EU's campaigns and "
              "the content that took Hano Crypto to %s followers, so the site and the "
              "campaign speak the same visual language rather than being commissioned "
              "separately." % PROOF["followers"]]),
        ],
        faqs=[
            ("Do you build the website or just design it?",
             "Both. We design and build, then launch. You are not left holding a design "
             "file and a quote from a separate developer."),
            ("Do you do blockchain or smart contract development?",
             "No. We design and build front-end websites and experiences, including "
             "connecting to services you already use. Smart contract development and "
             "auditing is specialist security work and we would refer you to a firm "
             "that does it properly."),
            ("How long does a website take?",
             "A focused landing page can be weeks; a full brand site depends on scope "
             "and content readiness. We agree direction before build starts, which is "
             "where most timeline overruns actually come from."),
            ("Can you work with our existing brand?",
             "Yes. We work inside an existing identity, or build one first if you do "
             "not have a system that survives being animated."),
            ("Will the site be fast on mobile?",
             "That is a requirement, not an aspiration. Performance is treated as a "
             "design constraint from the first conversation, because a crypto audience "
             "is mobile-first and impatient."),
        ],
    ),
]


def build_page(svc, head, tail):
    """Return the full HTML for one service page."""
    url = "%s/services/%s.html" % (BASE, svc["slug"])

    # Rewrite the shared head for this page.
    h = head
    h = re.sub(r"<title>.*?</title>", "<title>%s</title>" % svc["title"], h, flags=re.S)
    h = re.sub(r'<meta name="description" content=".*?">',
               '<meta name="description" content="%s">' % svc["desc"], h, flags=re.S)
    h = re.sub(r'<link rel="canonical" href=".*?">',
               '<link rel="canonical" href="%s">' % url, h)
    h = re.sub(r'<meta property="og:url" content=".*?">',
               '<meta property="og:url" content="%s">' % url, h)
    h = re.sub(r'<meta property="og:title" content=".*?">',
               '<meta property="og:title" content="%s">' % svc["h1"], h, flags=re.S)
    h = re.sub(r'<meta property="og:description" content=".*?">',
               '<meta property="og:description" content="%s">' % svc["desc"], h, flags=re.S)
    h = re.sub(r'<meta property="og:image" content=".*?">',
               '<meta property="og:image" content="%s/assets/img/og-image.jpg">' % BASE, h)
    h = h.replace('<meta property="og:type" content="article">',
                  '<meta property="og:type" content="website">')

    # Replace the case-study JSON-LD with Service + FAQPage + breadcrumbs.
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Service", "@id": url + "#service",
             "name": svc["h1"], "url": url,
             "description": svc["desc"],
             "serviceType": svc["keywords"][0],
             "provider": {"@id": ORG},
             "areaServed": "Worldwide",
             "inLanguage": "en"},
            {"@type": "FAQPage", "@id": url + "#faq",
             "mainEntity": [
                 {"@type": "Question", "name": q,
                  "acceptedAnswer": {"@type": "Answer", "text": a}}
                 for q, a in svc["faqs"]]},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Services",
                  "item": BASE + "/#services"},
                 {"@type": "ListItem", "position": 3, "name": svc["h1"], "item": url}]},
        ]}
    # Passed as a lambda, not a string: re.sub interprets backslashes in the
    # replacement, and JSON containing a \u escape (an em dash, say) raises
    # "bad escape \u". A callable is substituted literally.
    ld = ('<script type="application/ld+json">\n%s\n</script>\n'
          % json.dumps(graph, indent=2))
    h = re.sub(r'<!-- Case-study structured data.*?</script>\n',
               lambda _m: ld, h, flags=re.S)

    # Body.
    secs = []
    for heading, paras in svc["sections"]:
        body = "\n".join("    <p>%s</p>" % p for p in paras)
        secs.append('  <section class="case-sec">\n    <h2>%s</h2>\n%s\n  </section>'
                    % (heading, body))

    # Sibling services, so the six pages form a connected cluster rather than
    # six spokes off the homepage. Built from SERVICES so adding a page here
    # automatically appears on all the others.
    siblings = "\n".join(
        '      <li><a href="%s.html">%s</a></li>' % (o["slug"], o["nav"])
        for o in SERVICES if o["slug"] != svc["slug"])

    faq_items = "\n".join(
        "      <details%s>\n        <summary>%s</summary>\n        <p>%s</p>\n      </details>"
        % (" open" if i == 0 else "", q, a)
        for i, (q, a) in enumerate(svc["faqs"]))

    main = """<!-- ============ SERVICE ============ -->
<!-- Generated by tools/make-service-pages.py — edit that file, not this one. -->
<article class="case">

  <a class="case-home" href="../index.html" aria-label="Hano Studios — back to home">
    <img src="../assets/logo/logomark_white.png" alt="">
  </a>

  <header class="case-row">
    <div class="case-brand">
      <p class="case-kicker">%s</p>
    </div>
    <div class="case-intro">
      <h1>%s</h1>
      <p class="case-lead">%s</p>
    </div>
  </header>

%s

  <section class="case-sec">
    <h2>Common questions</h2>
    <div class="faq-list svc-faq">
%s
    </div>
  </section>

  <section class="case-sec">
    <h2>Related work</h2>
    <ul class="svc-links">
      <li><a href="../work/hano-crypto.html">Hano Crypto &mdash; 0 to %s followers, %s views</a></li>
      <li><a href="../work/bybit.html">Bybit &mdash; two campaigns for a global exchange</a></li>
      <li><a href="../work/kalshi.html">Kalshi &mdash; crypto content for a $22B exchange</a></li>
      <li><a href="../work/the-crypteum.html">The Crypteum &mdash; 400 to %s in three months</a></li>
    </ul>
  </section>

  <section class="case-sec">
    <h2>Other services</h2>
    <ul class="svc-links">
%s
    </ul>
  </section>
</article>
""" % (svc["kicker"], svc["h1"], svc["lead"], "\n\n".join(secs), faq_items,
       PROOF["followers"], PROOF["views"], PROOF["crypteum"], siblings)

    return h + main + tail


def main():
    head, tail = shell()
    outdir = os.path.join(ROOT, "services")
    os.makedirs(outdir, exist_ok=True)
    for svc in SERVICES:
        path = os.path.join(outdir, svc["slug"] + ".html")
        open(path, "w").write(build_page(svc, head, tail))
        print("wrote services/%s.html" % svc["slug"])


if __name__ == "__main__":
    main()
