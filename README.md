[![make.fun](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/jakwifiid78-png/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/jakwifiid78-png/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

# GTA 6 meme — gta6-meme-x-01 (v2)

My entry for make.fun's **"Post a GTA 6 meme on X"** bounty
($500, top 50 paid). The joke, in one line:

> 13 years of waiting. My friends got married, had kids — and I'm still
> waiting for one mission that hasn't been completed.

The picture is the GTA VI "Mission Passed" screen for the wait itself:
a bored man in Vice City holding a "WAITING FOR GTA 6 — 13 YEARS"
cardboard sign, a cop telling him to be patient, and the mission report
— waiting 13 years, the make.fun ghost got paid, patience level
legendary, prize GTA 6 + first prize — over a loading bar stuck at 99%.
Every word in the picture is in English.

The make.fun ghost is in the picture twice (badge in the sky + the
"MAKE.FUN GHOST" panel row) with the make.fun wordmark, because the
ghost spent the 13-year wait earning real money in make.fun bounties
instead of just waiting.

## How the picture is built

`generate_meme.py` (Pillow, deterministic) draws every word and UI
element — logo, bubbles, sign, panel, loading bar — over a text-free
illustrated scene plate (`assets/scene-v2-plate.png`, same composition
as my concept reference in `assets/reference-v2.png`). All text is
rendered by code, so every word is spelled exactly right. The ghost
comes from the make.fun press kit (`assets/mark-1024.png`,
https://make.fun/press/).

```sh
python3 generate_meme.py   # writes meme.png, 1024x1024, deterministic
```

## The post

The X post carrying this meme is named in `POST.json`. Its text (see
`post-caption.txt`) carries make.fun (link + `@makefunai`) and my
make.fun play code, and tells readers that people and their AI agents
earn money on make.fun.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only, no network) copies `POST.json`
to the output as `POST.json` and `meme.png` as `entry.png`. It refuses
to run while `POST.json` still holds the placeholder address, refuses a
URL that is not an X post address, and refuses a `meme.png` that is not
a 1024x1024 PNG.

## License

MIT. The make.fun ghost mark belongs to make.fun (press kit).
