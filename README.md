# Reference Angle

Browser tool for figure artists. Rotate a 3D head, get real photographs at that camera angle. Real photos. No AI generation.

**Live:** referenceangle.art *(URL pending)*

ReferenceAngle.com went offline. Artists who used it daily had no replacement. This is the revival.

---

## Credits

**Revived and hosted by:** [Watusi / Extendo](https://extendo.bet)
Donations: [ko-fi.com/vivacarta](https://ko-fi.com/vivacarta)

**Original author:** [x6udpngx](https://github.com/x6ud) built the tool. The editor, the pose search, all of it.
Donations: [ko-fi.com/x6udpngx](https://ko-fi.com/x6udpngx)

**Special thanks:** [xrabohrok](https://github.com/xrabohrok)

Original repo: [x6ud/search-photos-by-model-tool](https://github.com/x6ud/search-photos-by-model-tool)

---

## What's in this repo

This is the lite version. 553 portrait photos from FFHQ, indexed by yaw/pitch/roll. Small enough to clone and host free.

Full version is 50,001 photos. That set lives offline. To build your own full version, run the pipeline in `pipeline/`.

---

## Run locally

```bash
npm install
npm run serve
```

Visit http://localhost:8080.

## Build for production

```bash
npm run build
```

Output is in `dist/`. Static. Drop it on any host.

---

## Build a custom dataset

The `pipeline/` folder has the Python tooling. Install from `pipeline/requirements.txt`.

1. Drop photos in `pipeline/input/`
2. Run `extract_poses.py`. MediaPipe does the pose math.
3. Output writes to `src/data/human.json`
4. Copy the indexed photos into `static/pipeline/input/`
5. `npm run build`

---

## Editor mode

`/#/editor` for manual photo tagging. Needs a Flickr API key for the search step.

---

## License

See LICENSE. Revival respects the original terms.
