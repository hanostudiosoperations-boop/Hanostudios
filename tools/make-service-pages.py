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
    h = re.sub(r'<!-- Case-study structured data.*?</script>\n',
               '<script type="application/ld+json">\n%s\n</script>\n'
               % json.dumps(graph, indent=2), h, flags=re.S)

    # Body.
    secs = []
    for heading, paras in svc["sections"]:
        body = "\n".join("    <p>%s</p>" % p for p in paras)
        secs.append('  <section class="case-sec">\n    <h2>%s</h2>\n%s\n  </section>'
                    % (heading, body))

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
</article>
""" % (svc["kicker"], svc["h1"], svc["lead"], "\n\n".join(secs), faq_items,
       PROOF["followers"], PROOF["views"], PROOF["crypteum"])

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
