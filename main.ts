// Frost Front Page — news-image-20261123.
//
// The whole front page is pre-rendered: draw_20261123.py paints the
// 1024x1024 PNG with PIL, and this file is the only thing the grader
// runs. Its job is deliberately tiny — copy that one image into the
// output directory — so the run is deterministic, offline and has no
// third-party dependencies. Node 22 standard library only.

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The image lives next to this file in the repository.
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

// The grader mounts the output directory here; honour the override
// when one is set so local runs can point anywhere.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts (${source})`);
}

mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);

// The entry must stay a single 1024x1024 PNG under 1 MiB. Refuse to
// report success if the copy somehow came out over the cap.
const bytes = statSync(target).size;
if (bytes > 1024 * 1024) {
  throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB cap`);
}
console.log(`wrote ${target} (${bytes} bytes)`);
