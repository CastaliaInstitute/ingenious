# Issue 1: revised edition production record

## Scope and status

The authoritative source is Chapter One, including its two interludes, in
`novel/THE_INGENIOUS_MACHINE.md`. The September 8 revision gives Q an existing
conversational relationship with the Custodian, an unfamiliar body, competent
language, and a chosen journey. It establishes the workshop key and pocket repair.
The rest of the novel now allows the book to end while Q continues living.

This edition is a revision proof, not an A+ press master. Do not automatically
send it to the Epson. Screen review does not establish fine-line reproduction,
paper opacity, ink density, or actual printer feed and duplex behavior.

## Fixed Issue 1 specification

- Trim: 6.625 x 10.25 inches (477 x 738 PDF points).
- 24 pages: illustrated cover; eleven continuous narrative pages paired with
  eleven unique facing plates; one final publication-information page.
- Twelve plates including the cover, not twelve narrative pages plus a cover.
- Narrative on pages 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, and 22; facing art on
  pages 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, and 23.
- Georgia 12-point body type on 17-point leading; two columns, ragged right.
  Paragraphs continue between columns and narrative pages. No forced chapter or
  interlude page starts; headings stay with following text.
- Text-page backgrounds are unpainted. Cream is supplied by the paper, never a
  page-sized colored rectangle or texture. Black text remains vector text.
- Art reaches the comic trim edges. Each caption is separately typeset in an
  inset white margin strip; no caption is generated into the raster.
- A3 landscape: each two-page comic spread centered at actual size. Fold ticks
  and sheet labels are outside the comic trim. Folding A3 produces a larger
  A4-size carrier around the centered comic trim; trimming is a separate step.
- Twelve A3 PDF sides, six sheets with duplex enabled. Print all sides at actual
  size, short-edge duplex. The PDF contains no reverse-side rotation. Physical
  stack order still depends on the selected printer's output-tray behavior.

## Booklet order

| Sheet | Outside | Inside |
| --- | --- | --- |
| 1 | 24, 1 | 2, 23 |
| 2 | 22, 3 | 4, 21 |
| 3 | 20, 5 | 6, 19 |
| 4 | 18, 7 | 8, 17 |
| 5 | 16, 9 | 10, 15 |
| 6 | 14, 11 | 12, 13 |

## Facing-art source of truth

`output/illustrations/revised/issue-01/manifest.json` records the chapter hash,
actual rendered text opposite each plate, source block identifiers, caption,
prompt, asset path, and review status. The cover brief was reconstructed from
the generation record; interior prompts are recorded exactly. Built-in image
generation was used, with the corrected cover as a character reference.

Q retains the segmented oval head, circular ear mechanisms, exposed neck,
articulated hands, question-mark breastplate, and long-limbed proportions. The
Custodian is consistently a tall man with long gray hair, glasses, white work
shirt and boots. Roque is a distinct short-haired night guard. Nayeli is the
maintenance worker watching Q use the handrail, not a substitute Custodian.

Generation requests clean black-and-white art. Print production must additionally
enforce DeviceGray in the PDF: apparent neutrality on screen alone is not proof
that an RGB raster will use only black ink. Original generated assets remain
unchanged. These approximately 1K x 1.5K plates provide about 150 dpi at trim;
do not mislabel interpolation as newly generated 300-dpi detail.

## Verification and reproducibility

Development tools remain in `/tmp` under repository instructions:

- `/tmp/build_ingenious_issues_v2.py`: continuous pagination, explicit manifest
  validation and A3 imposition. Rejects stale source hashes, unreviewed assets,
  duplicate image hashes, missing plate IDs and incorrect Issue 1 page count.
  It never repeats assets using modulo indexing.
- `/tmp/qa_ingenious_issue1.py`: independent pdfplumber extraction compared with
  source order; text-page fill/image checks; page-size, count and rotation checks;
  booklet-pair checks; optional DeviceGray checks on final plate objects.

The builder extracts each rendered text page for its illustration map.
ReportLab's `Paragraph.getPlainText()` can return empty text for split paragraphs;
using it directly would omit facing-text fragments even when the PDF looks right.
Rendered extraction is checked against the complete source token sequence.
The independent checker confirmed 3,836 words in the layout proof. All eleven
narrative pages were rendered and visually inspected. Final image insertion and
print-color conversion require the same checks again.

The tools' temporary location is not a durable build distribution. The production
specification and manifests are retained here; preserve the scripts separately
before clearing `/tmp`. Old builders and old PDF filenames must not silently
overwrite the revised edition or be presented as current.

## Verified revision-proof outputs

After art insertion and grayscale conversion, the independent check again found
all 3,836 narrative words in order, no text-page fills or images, twelve DeviceGray
plate objects, 24 comic pages, twelve A3 landscape sides, the six sheet pairs
above, and no rotated PDF pages. All twelve plate pages were rendered and
inspected with their captions; the cover was re-rendered after removing an opaque
title mask that clipped the antenna. The cover, first reverse, and central A3
spread received visual review. No physical print test is claimed.

- Reading proof: `output/pdf/ingenious-issue-01-revised-en-bw.pdf`
  SHA-256: `78bd883e43a118a7dc9574c405cc5574cfdd71e037c3423871ec4122111fe733`.
- A3 proof: `output/pdf/ingenious-issue-01-revised-en-bw-a3.pdf`
  SHA-256: `17dd1f3724045a37658ad0c16c374dea1d2e3fc8708c0d3fe06be66ddd6503c4`.

Final preflight also rejects JPEG re-encoding. Ghostscript's grayscale print
conversion uses `ColorConversionStrategy=Gray`, disables all image downsampling,
and sets `AutoFilterGrayImages=false` with `GrayImageFilter=/FlateEncode` (and
the equivalent color filter settings). This preserves the native generated
resolution with lossless compression of the grayscale plate data. It does not
create higher-resolution detail. The original RGB PNG assets remain unchanged.
