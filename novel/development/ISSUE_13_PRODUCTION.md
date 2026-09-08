# Issue Thirteen: verified illustrated revision proof

Author: A. Cervantes. Source: Chapter Thirteen and both interludes in the current
English manuscript. Editorial scope: `CHAPTER_13_ENCOUNTER_REVIEW.md`.

## Deliverables

- Reading: `output/pdf/ingenious-issue-13-revised-en-bw.pdf`
- A3: `output/pdf/ingenious-issue-13-revised-en-bw-a3.pdf`
- Twelve selected PNGs and complete prompts/reference/edit provenance:
  `output/illustrations/revised/issue-13/manifest.json`

Reading SHA256:
`8e78673dad6fae25d8f418ac3dfe0a4dbc7976cc30ff1ff2c9154e292c35eb32`

A3 SHA256:
`1f3e38cf22ff0706319554e061b71e9af5569522ec2beb53825aef18a5d88560`

Chapter SHA256:
`254cd96f65f84c55423ee48b2750ac9d79f3cd70ed099fa66d212a0cc7d44601`

## Layout

24 pages: cover, eleven continuously flowing two-column text pages alternating
with eleven unique facing plates, and publication information. All 3,773 narrative
words remain in source order. Georgia 12.7/17.9917 points; five reading-PDF font
subsets are embedded. No forced interlude page starts. The last narrative page
occupies both columns. Narrative backgrounds contain no fills, rectangles or
images; cream comes from the paper, not printed tint.

Comic trim is 477 x 738 points. Art reaches all four trim edges, with captions in
separate inset white bottom strips. Native selected PNGs are 1024 x 1536 pixels.
The finished PDF retains those dimensions as twelve lossless DeviceGray images,
without JPEG conversion or downsampling. This is roughly 150 dpi at trim, not a
300-dpi press master. No synthetic enlargement is represented as recovered detail.

A3 pages are landscape, 1190.55118 x 841.88976 points, centered at actual size.
Twelve sides make six duplex sheets using short-edge flip. Pairs, in file order:

| Sheet | Outside | Inside |
| --- | --- | --- |
| 1 | 24 / 1 | 2 / 23 |
| 2 | 22 / 3 | 4 / 21 |
| 3 | 20 / 5 | 6 / 19 |
| 4 | 18 / 7 | 8 / 17 |
| 5 | 16 / 9 | 10 / 15 |
| 6 | 14 / 11 | 12 / 13 |

The fold produces an A4-size carrier around the smaller comic trim. Trimming is a
separate operation. Fold marks and print instructions sit outside the comic trim.
No page has a rotation flag. These are already imposed spreads: a printer driver
must not apply another booklet or multiple-pages-per-sheet transformation.
Physical driver configuration and output-stack order remain untested.

## Artwork review

Built-in reference-based generation produced twelve initial images. Two targeted
edits corrected Ofelia's initials and the private video call's camera geometry.
Every final selected image was inspected at native resolution before insertion.
The original generated variants remain in their generated-image locations; only
the selected PNGs are referenced by the project.

Q wears the short fitted dark jacket, not the obsolete long coat in the earlier
plan. His right knee remains supported when visible. Lucía and Ofelia follow
earlier character references. Rebeca recurs across the notebook and performance
plates. Alma recurs across arrival, departure and the later receipt visit. The
unnamed training nurse is visually distinct. The tall male Custodian appears only
on the private call screen, with long gray hair and glasses.

The deposited hospital photograph, identifiable medical number and disclosed
lease are not displayed. The handwriting initials and all document mark-making
are illustrative, not archival facsimiles. Alma's later sister visit is not
collapsed into the earlier hospital event; neither Q nor the Custodian is added
to that coda without textual support.

## Verification performed

- Independent two-column extraction matches all 3,773 source words in order.
- All eleven exact facing texts, block-ID lists and scene anchors match the
  current layout; all twenty-two issue manifests match newly generated plans.
- All twelve asset hashes, distinctness and native dimensions match the manifest.
- Twelve image pages contain exactly one DeviceGray image each; lossless filters
  and original pixel dimensions are preserved. Reading fonts are embedded.
- All twenty-four reading pages were rendered at 95 dpi and inspected; all twelve
  A3 sides were rendered at 75 dpi and inspected. Titles, captions, text flow,
  clipping, readable column spacing and upright placement were checked.
- Every actual A3 slot was compared with its source reading page: extracted text,
  decoded image hash, image count, translation and explicit trim clipping. Printed
  pair labels alone were not treated as proof of correct imposition.
- Only Chapter Thirteen changes against `cf9f5d05`; the other twenty-one chapters,
  final pen sentence and twenty-four current Issues 1-12 PDF files are unchanged.

The temporary builder and verification scripts remain under `/tmp` per repository
instructions: `build_ingenious_issues_v2.py`, `qa_ingenious_issue1.py`,
`check-ingenious-issue13-source.mjs`, `check-ingenious-issue13.py`, and the Issue 13
finalize/contact-sheet scripts. Grayscale conversion used Ghostscript with Flate
filters and color/gray/mono downsampling disabled. Final proof renders and layout
metadata remain in `/tmp/ingenious-issue13-final`.

## Limits and next work

No print job was sent. This pass is not an independent faculty review, new blind
simulation or A+ certification. Press-resolution and ink-on-stock review, broader
literary evaluation, nine later illustrated issue builds and a revised Spanish
edition remain open. The active goal is not complete.
