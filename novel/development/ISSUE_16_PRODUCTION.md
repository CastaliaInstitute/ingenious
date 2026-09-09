# Issue Sixteen: illustrated hearing revision proof

Date: 2026-09-08. Baseline: `da046439`.

Chapter: *The Trial of the Machine*, including *The Form Without a Category*.
Source SHA-256: `bd53369485c17976d915ad1d3d2f61c19ad59e5e00993341bb930d96675be41c`.
This production pass does not change the English manuscript or outline.

## Deliverables

- `output/pdf/ingenious-issue-16-revised-en-bw.pdf`: 20 reading pages.
- `output/pdf/ingenious-issue-16-revised-en-bw-a3.pdf`: ten A3 landscape sides,
  imposed as five nested duplex sheets.
- `output/illustrations/revised/issue-16/`: ten unique native PNGs, including
  the cover, and a manifest of full prompts, references, edits, hashes and reviews.

All 3,051 words flow through nine two-column narrative pages. Georgia 12.4 points
on 17.5667-point leading, 197-point columns, 15-point gutter and 34-point side
margins. Three short dialogue groups stay within a column. No manual page breaks
were added. The interlude follows the prose without starting a new page.

Comic trim is 477 by 738 points (6.625 by 10.25 inches). Images fill trim, with
separately typeset captions in inset white strips. Narrative backgrounds are
unpainted, not simulated cream. The native RGB images retain some warmth despite
the requested palette; the PDFs convert them to neutral DeviceGray without
downsampling or JPEG recompression. Tonal texture within illustrations remains.

The user's question about justification was answered too generally before the
saved trial was checked. That trial showed distracting gaps at this narrow
measure, despite English hyphenation. Production therefore retains the reviewed
left alignment. This does not reject all possible justified compositions.

## Fold layout

Each 954-by-738-point spread is centered on A3 landscape and clipped to trim.

| Sheet | Outside | Inside |
| --- | --- | --- |
| 1 | 20 / 1 | 2 / 19 |
| 2 | 18 / 3 | 4 / 17 |
| 3 | 16 / 5 | 6 / 15 |
| 4 | 14 / 7 | 8 / 13 |
| 5 | 12 / 9 | 10 / 11 |

Print all ten sides at actual size, landscape, duplex short edge, without applying
a second booklet layout. These files verify pairing and orientation, not the
Epson's actual output-tray stacking or duplex behavior. No print job was sent.

## Art and scene fidelity

The built-in image generator produced ten scenes and two targeted corrections.
Goya's Capricho 43 supplies graphic language; earlier drawings supply identity.
The museum source, native reference and attribution are recorded in
`GOYA_ART_DIRECTION.md` and the Goya pilot manifest. No CLI/API fallback was used.

| Plate page | Facing text | Action |
| --- | --- | --- |
| 1 | Cover | Q among ordinary tables under the cinema's large blank screen |
| 3 | 2 | Clerk moves a cable while Q rests his right foot on a low stool |
| 5 | 4 | Remote water vendor Hilario makes change during testimony |
| 7 | 6 | Chano offers a paper cup after naming their friendship |
| 9 | 8 | Male Custodian reads the original day-trip permission in person |
| 11 | 10 | Q slides the seminar exhibit reference toward his adviser |
| 13 | 12 | Testimony compares the obstructed camera view with other records |
| 15 | 14 | Q answers what he still wants, leaving the notes on the table |
| 17 | 16 | Lucía hands over permitted copies; Chano retains two notices |
| 19 | 18 | Secretary moves lunch away from copier and napkin-shadow copy |

The first Hilario image placed the cold-water container on the table; the edit
moves it underneath. The first handoff resembled a bound book; its replacement
shows a flexible tabbed folder containing separate sheets. Neither edit changed
the facing passage or invented a new story event.

Q retains the panel-built oval head, round ears, mechanical mouth, slim body and
short long-sleeved jacket. His independent adviser has short silver-brown hair
and rectangular glasses, distinct from Lucía's longer dark hair and denim jacket.
The Custodian is tall, male, long-haired and bespectacled. His testimony is in
person; he is not inserted into the later folder handoff before the remote call.
Hilario is the lean water vendor, not the retired miner of the same name.

No turbine charge is illustrated as an actual incident, no private inquiry is
exposed on screen, and neither the delivered module nor original Tijuana ledger
reappears in the characters' possession. The quiet Q portrait faces his answer
on text page 14; the additional wish to go out without bringing back a chapter
follows on page 16. It is not illustrated as an already completed departure.

## Verification

All ten selected native images, twenty reading pages and ten A3 sides were
visually inspected. Cover title placement, captions, trim, grayscale appearance,
white text backgrounds and continuous prose were checked. Automated verification
establishes exact source-order extraction; unchanged facing-text/block mappings;
ten distinct native raster payloads; lossless DeviceGray image storage; embedded
fonts; and correct text, decoded image, translation and clipping in all twenty
actual A3 page positions. Page rotations are zero. Five reading-font subsets and
six A3-font subsets are embedded. The three short-exchange groups remain together.

All 22 chapter texts and issue bindings, the outline, the living final sentence,
and all 30 preceding issue reading/A3 PDFs are unchanged from `da046439`.

Reading SHA-256: `85aaa77a896f0e22f3d5386e9f8efc3f2b2dcc5ad9b2a83ebade52e174adaa2f`.
A3 SHA-256: `92fb7b4c5136c0145dbdf6a79ac42dc72dc0a6ae4fbdabd1998637aa08ee59a8`.

Temporary build, renders and verification remain in `/tmp/ingenious-issue16-final`.
Builders: `/tmp/build-ingenious-issue16-final.py` and
`/tmp/build_ingenious_issues_v2.py`. Verifier:
`/tmp/check-ingenious-issue16-final.py`. PDF output copies are checked byte-for-byte
against the inspected temporary proofs. Skill-directed image review and full
PDF rendering governed selection, correction and verification.

## Limits and continuing literary work

This is an illustrated revision proof, not an A+ certification or a press master.
Each native image is 1024 by 1536 pixels, approximately 150 dpi at trim. Increasing
pixel dimensions alone would not establish new detail. Some faces and settings
remain more naturalistic/descriptive than Goya's most economical prints; the
whole-series art review must retain that distinction rather than equating a
technical pass with artistic completion.

The hearing has human interruptions and Q's wish for life beyond the book, but
its many procedural distinctions may still tax a general reader. The next broad
literary pass should assess cumulative pace and cast recall across adjacent
chapters, preserving consequential distinctions rather than replacing them with
a triumphant summary. This pass adds no new scene simulation or faculty approval;
the preceding ten inference calls and their limits remain documented in
`CHAPTER_16_FRESH_CONTEXT_REVIEW.md`.

Issue Fourteen still needs replacement art, Issues 1-13 need the governing style
audit, and Issues 17-22 need completed illustrated revision proofs. Broader
literary/simulation review and revised Spanish synchronization remain unfinished.
The full two-book goal remains active.
