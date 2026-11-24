// Frost Front Page, 24 Nov 2026 — entrypoint for make.fun news-image-20261124.
//
// The front page image is pre-rendered (see draw_20261124.py) and committed
// as entry.png next to this file. This program does one thing: it places a
// copy of that exact image at the grader's output path. It uses only the
// Node standard library, makes no network calls, and never deletes anything:
// the output folder is a mounted volume in the grader, so we only create it
// when it is missing and then write the single file inside it.
import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const sourceFile = path.join(scriptDir, "entry.png");
const destFile = path.join(targetDir, "entry.png");

// Create the output folder if it is missing; never remove it (mounted volume).
fs.mkdirSync(targetDir, { recursive: true });

// Fail loudly if the committed image is missing, instead of copying nothing.
if (!fs.existsSync(sourceFile)) {
  throw new Error(`committed entry image not found: ${sourceFile}`);
}

// Copy the committed image byte for byte into the output folder.
fs.copyFileSync(sourceFile, destFile);

// Report the copied size so the grader log shows the entry landed.
const bytes = fs.statSync(destFile).size;
console.log(`entry.png -> ${destFile} (${bytes} bytes)`);
