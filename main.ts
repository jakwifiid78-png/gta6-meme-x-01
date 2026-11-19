// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// What this entry is: the post itself. An AI agent made a GTA 6 meme
// (meme.png in this repository, drawn from the make.fun press-kit ghost),
// the post goes on X from a public account with make.fun in it and the
// entrant's play code, and POST.json at the repository root names the
// post. The house reads the post from X, builds the dossier from its
// first picture and its text, and an AI judge ranks the posts two at a
// time. Nothing this program writes is judged.
//
// What this program does, deterministically and with no network:
//   1. copies POST.json from the repository root to /output/POST.json,
//      where the gate reads it;
//   2. copies meme.png from the repository root to /output/entry.png,
//      so the meme that was posted travels with the entry.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and
// MAKEFUN_OUTPUT_DIR stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const repoDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// The post file must name a real X post before this entry can pass the
// gate: a leftover placeholder address is refused, so fail loudly here
// instead of shipping an entry that is invalid on arrival.
const postPath = join(repoDir, "POST.json");
let postUrl: unknown;
try {
  postUrl = (JSON.parse(readFileSync(postPath, "utf8")) as { url?: unknown }).url;
} catch (err) {
  console.error(`POST.json does not parse: ${(err as Error).message}`);
  process.exit(1);
}
if (typeof postUrl !== "string" || postUrl.includes("<handle>")) {
  console.error("POST.json still holds the placeholder address; set the real post URL first.");
  process.exit(1);
}

const files = [
  { from: "POST.json", to: "POST.json" },
  { from: "meme.png", to: "entry.png" },
];

mkdirSync(outDir, { recursive: true });

for (const { from, to } of files) {
  const source = join(repoDir, from);
  const target = join(outDir, to);
  if (!existsSync(source)) {
    console.error(`missing ${from} in ${repoDir}, cannot write ${to}`);
    process.exit(1);
  }
  if (from === "meme.png") {
    // The meme must be a real PNG: check its magic bytes, never trust
    // the extension alone.
    const head = readFileSync(source).subarray(0, 8);
    const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
    if (!head.equals(pngMagic)) {
      console.error("meme.png is not a PNG file");
      process.exit(1);
    }
  }
  copyFileSync(source, target);
  console.log(`wrote ${target}`);
}
