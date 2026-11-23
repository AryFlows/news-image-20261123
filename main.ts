// Frost Front Page - Monday 23 November 2026.
// Copies the pre-rendered entry.png to the output directory.
// Standard library only; deterministic: same bytes every run.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry: 21 verified stories for 23 November 2026, 1024x1024 PNG.
// Rendered by render_v2.py; this file only copies it into place.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
