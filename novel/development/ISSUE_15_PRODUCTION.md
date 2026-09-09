# Issue Fifteen: complete illustrated revision proof

Date: 2026-09-08. Baseline: `e178b3a3`.

Chapter: *The Cave of the Corpus, Reopened*, including *The Catalog of Lost Things*.
Source hash: `32a02ca60bdced6c1631e9f75452d55548a027132c9513df59244cf2e5985ba1`.
The English manuscript text is unchanged in this production pass.

## Deliverables and layout

- `output/pdf/ingenious-issue-15-revised-en-bw.pdf`: 16 reading pages.
- `output/pdf/ingenious-issue-15-revised-en-bw-a3.pdf`: 8 A3 landscape sides,
  imposed for a four-sheet nested booklet.
- `output/illustrations/revised/issue-15/`: eight distinct native PNGs and the
  manifest containing prompts, references, corrective edits, hashes and reviews.

All 2,481 words flow in exact source order through seven two-column text pages.
Georgia 12.3 points on 17.425-point leading; 197-point columns, 15-point gutter,
34-point side margins. Body text remains left-aligned. The interlude starts where
the text reaches it, without a forced page break. Comic pages are 477 by 738
points (6.625 by 10.25 inches). Plate canvases fill trim; captions are separately
typeset in a white margin strip. Paper-white areas are intentional reserves, not
simulated cream stock. Text pages have no background images or filled rectangles.

A3 pages are 1190.55118 by 841.88976 points. Each 954-by-738-point spread is
centered at actual size, clipped to comic trim. Outside/inside pairs:

| Sheet | Outside | Inside |
| --- | --- | --- |
| 1 | 16 / 1 | 2 / 15 |
| 2 | 14 / 3 | 4 / 13 |
| 3 | 12 / 5 | 6 / 11 |
| 4 | 10 / 7 | 8 / 9 |

Use landscape, actual size, duplex short edge, all eight sides. Do not apply
booklet imposition again. This file establishes page pairing, not the Epson's
output-tray order or duplex behavior. Those require a physical test. Nothing was
printed in this pass.

## Art and facing scenes

The built-in image generator produced six new assets, using the actual Goya
Capricho 43 print for graphic language and the corrected Q drawing for identity.
It also corrected the laptop lid. Existing phone and lunch drawings were retained
and rechecked with the full set. Full prompts are saved in the manifest.

| Plate page | Facing text | Caption and action |
| --- | --- | --- |
| 1 | Cover | Ordinary ministry entrance and booklet machine |
| 3 | 2 | Daylight in either version: Inés raises a rechargeable lamp |
| 5 | 4 | What remains: Q and colleagues check the preservation list |
| 7 | 6 | Still writing: private call to the remote Custodian |
| 9 | 8 | Yesterday's reminder: Inés finds two slips and calls the signer |
| 11 | 10 | Opinions about lunch: suadero and a small amount of salsa |
| 13 | 12 | The next sheet: Q continues checking permitted summaries |
| 15 | 14 | One orange and a bag: Mauro peels while Prime carries |

Q retains the segmented narrow head, circular ears, mechanical sampling mouth,
long neck and short long-sleeved jacket. Prime belongs to the same head family
but has cleaner light plating, no jacket, no injury support. Inés has a short bob
and no glasses; Marisol has a low bun and square glasses. Mauro is compact with
short curls, a close beard and wire glasses, not the tall long-haired Custodian.

The drawings do not show a loss of intelligence or personal memory. The papers
contain no legible private family testimony. No invented hidden archive, medieval
costume, ritual sacrifice, or food-as-battery imagery was added.

## Verification

All eight native images, sixteen reading pages and eight A3 sides were visually
inspected. Captions, cover typography, text continuity, whitespace and cropped
edges were checked. The final extraction and content-stream checks establish:

- Every narrative word appears once, in source order; all seven facing passages,
  block IDs and scene anchors match the existing plan.
- Eight distinct native raster payloads in the original assembly match their
  selected PNGs exactly. Final PDFs preserve native dimensions, lossless
  DeviceGray images, and no JPEG recompression or downsampling.
- Every A3 slot has the correct text, decoded image and translation, with a
  477-by-738-point clipping path and zero page rotation.
- Five reading-font subsets and six A3-font subsets are embedded. The additional
  A3 subset supplies production labels; an unused default Helvetica resource
  was eliminated by initializing the label canvas with the embedded font.
- All 22 chapter texts and all 22 issue bindings are unchanged from the baseline.
  The living ending remains intact. All 28 preceding reading/A3 PDFs and the
  earlier two-scene study are unchanged.

Reading SHA-256: `7dc9a94604058f24ea2c256e7b87b8314212acb1632341c23e40372a0a686b60`.
A3 SHA-256: `4b2a4c3eb529fd74bf5a70ccb650abee17052e03b05feaf657ac217e04b521cd`.

Temporary build, render and QA files stay in `/tmp/ingenious-issue15-final`.
The build uses `/tmp/build-ingenious-issue15-final.py` and the continuous-layout
builder `/tmp/build_ingenious_issues_v2.py`; the verifier is
`/tmp/check-ingenious-issue15-final.py`. Grayscale conversion uses Ghostscript's
DeviceGray conversion with image downsampling disabled and Flate image filters.

## Limits and next literary review

This is a revision proof, not a press master or an A+ certification. Seven images
are 1024 by 1536 pixels; the lunch image is 1068 by 1473. Effective resolution is
approximately 144-150 dpi at trim. Enlargement alone would not provide new detail.
Some faces and architectural backgrounds remain more naturalistic/descriptive
than Goya's most economical prints; full-set artistic judgment remains necessary.

The shared jokes, unfinished attribution and chosen writing calls demonstrate
Q's agency more effectively than declarations that he has learned humanity.
However, the access-review passages still contain dense procedural exposition.
The next literary pass should test whether every explanation produces a lived
consequence, without replacing necessary causal distinctions with slogans. This
production pass is not a fresh scene simulation, faculty review or whole-book
literary approval. No new inference or faculty calls were made.

Issue Fourteen still needs replacement art, Issues 1-13 need the governing style
audit, and Issues 16-22 still need completed art and verified revision PDFs.
Broader literary/simulation review and revised Spanish synchronization remain
unfinished. The full goal remains active.
