# Launch Brief — Reference Angle
*Viva Carta / Extendo. May 2026.*

---

## What It Is

A browser-based tool for artists. Rotate a 3D head to any angle, get real photographs from that exact view. No AI imagery. No renders. Actual light on actual skin.

Built on FFHQ (70k public domain portrait photographs), indexed by yaw/pitch/roll via MediaPipe. The "database" is one flat JSON file. The viewer is Three.js. Deploy is static.

---

## Why Now

ReferenceAngle.com went dark. The artist community that depended on it has no replacement. That audience is still searching. The market is not hypothetical — it existed, used the product daily, and lost it. This is not building demand. It's filling a vacuum.

---

## The Positioning

**"ReferenceAngle is gone. We rebuilt it, and went further."**

That's the entire pitch for the launch post. One sentence. Everyone in the character art, concept art, and illustration community will recognize the name. The rest is proof.

What "further" means by launch:
- Larger dataset (FFHQ vs whatever that site had)
- Quality-filtered (blur detection, not raw scraped garbage)
- Free, no account, no friction
- Open pipeline published (the process is visible)

---

## Packaging Decisions

**Name:** Reference Angle (exact match to the dead tool, intentional)

**Domain:** `referenceangle.art` or `reference.angle` if available. Otherwise `referenceangle.vivacarta.net` for V1 while the domain resolves. Check availability before launch.

**Viva Carta branding:** Present but light. Footer attribution. The tool is the product. Brand awareness is the side effect, not the headline.

**Free to use:** No gate for V1. The value is in the dataset, the experience, and the community it builds. Monetization comes after trust.

---

## Launch Strategy

**Platform:** Threads, primary. This is Extendo's proven reach (600+ followers, 69k views on micrographic post). The art community lives on Threads and Instagram. The overlap is real.

**Format:** Video post. Show the head rotating. Show photos updating in real time. Caption is short. Something like:

> ReferenceAngle died. Spent the weekend rebuilding it.
> 70,000 real photographs, sorted by head angle.
> Rotate, get reference. No AI. Free.
> [link]

No thread. No explanation thread. The product explains itself on screen.

**Timing:** Ship when the loop is closed. Rotate head, photos render. That's the minimum for the post. Do not wait for Phase 2.

---

## Content Sequence After Launch

1. Launch post (video, as above)
2. Build post 24-48 hours later: how the pipeline works (MediaPipe, JSON index structure, why flat JSON instead of a database). Targets the builder audience. Positions Extendo.
3. Dataset post: FFHQ, what it is, why public domain matters for this. Builds trust with artists about the source material.
4. Open source post: publish the pipeline code. Invite people to run it on their own datasets.

Each post has a different function: post 1 captures artists, post 2 captures builders, posts 3-4 build credibility and community.

---

## Monetization Path (Phase 4, Not Now)

Free tier: full tool as launched.
Pro tier ($5-10/mo or one-time): access to expanded dataset with secondary tags (lighting type, skin tone range, focal length estimate). This is the Phase 3 differentiation layer from the init doc.

Ko-fi link present from day one. Not promoted heavily. Just there. Some artists will pay without asking.

Discord: Viva Carta server, channel for Reference Angle users. Power users, feedback loop, community. This is where artists become Viva Carta members.

---

## How This Fits

The art community is a new audience. Character artists, concept artists, illustrators. They're not in the Extendo design/builder feed yet. This tool is the entry point.

The funnel: tool user becomes Discord member, Discord member learns about Viva Carta, learns about the other tools (Timeline, future products). The reference tool is the widest door.

It also proves the Extendo model. Not just visual experiments. Actual useful tools that solve real problems. The micrographic engine showed craft. This shows utility. That combination is what builds a brand people trust.

---

## Definition of Done (Pre-Launch)

- Loop closed: rotate head, photos render from real index
- Deployed to domain (or subdomain), accessible via link
- Video captured (screen record, OBS, whatever)
- Launch post drafted and scheduled
- Ko-fi link in footer
- Discord invite in footer

---

## Open Questions

- Domain: `referenceangle.art` available? Check today.
- Dataset hosting: Vercel has a 100MB deployment limit. FFHQ subset (100 images for V1) should fit. Full 70k does not. CDN or Vercel large file support needed for Phase 2. Decide before Phase 2 build starts.
- Pipeline code: publish as Extendo GitHub repo or Viva Carta org? Recommendation: Extendo, with Viva Carta attribution in the README.
