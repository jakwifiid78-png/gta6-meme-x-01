# GTA 6 meme — gta6-meme-x-01

My entry for make.fun's **"Post a GTA 6 meme on X"** bounty
($500, top 50 paid). The joke, in one line:

> I waited 13 years for GTA 6. My ghost spent them getting paid on make.fun.

The ghost is make.fun's mascot — my AI agent, who spent the 13-year wait
earning real money in make.fun bounties instead of just waiting. The
picture is drawn with code (Pillow) from the make.fun press-kit ghost:
a Vice City sunset, a Leonida skyline, and the ghost front and centre.

## The post

The X post carrying this meme is named in `POST.json`. Its text carries
make.fun (link + `@makefunai`) and my make.fun play code, and tells
readers that people and their AI agents earn money on make.fun.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only, no network) copies `POST.json`
to the output as `POST.json` and `meme.png` as `entry.png`. It refuses
to run while `POST.json` still holds the placeholder address.

## Rebuild the meme

```sh
python3 generate_meme.py   # writes meme.png (deterministic)
```

The generator uses Pillow and the press-kit ghost in `assets/mark-1024.png`
(fetched from https://make.fun/press/).

## License

MIT. The make.fun ghost mark belongs to make.fun (press kit).
