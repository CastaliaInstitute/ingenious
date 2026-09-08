# Issue Ten: The Border Written in Air

## Editorial scope

Baseline: `804cb726`. The complete chapter, exact facing-page manifest and prior
production specification were read. The manuscript and outline are unchanged in
this production pass. The preceding fresh-context review supplies the evidence
for Q questioning the café wait; no new inference simulation or ask-faculty
review was run here. Salas's arrival remains authored, not a demonstrated
inevitability. See `CHAPTER_10_FRESH_CONTEXT_REVIEW.md` for those limits.

The issue gives space to the chosen Pacific stop, imperfect photograph and
successful delivery before the separate body-custody action. Q asks practical
questions, records an objection, warns about his knee and continues speaking
with people. His writing project does not require an incompetent decision or
death. The later return permits a shared drink, disagreement over the report,
and an appointment to write again. The whole novel's last line remains:
"The Custodian put down his pen."

The records interludes still occupy substantial space. Distinct illustrations
help distinguish the people and objects, but do not establish that the full
novel's rhythm is resolved. This is a verified illustrated revision proof, not
an A+ literary certification.

## Artwork and corrections

Fourteen unique full-page images were generated using the built-in image tool:
cover plus thirteen exact-facing interior scenes. The image-generation skill
guided reference-based identity preservation and targeted revisions. Q follows
the established segmented metal body, circular ears, question-mark breastplate
and articulated hands. He wears the fitted short jacket before transport and
removes it for restraint; it does not reappear on him during the return. Chano,
Lucía and the tall, long-haired male Custodian retain their established designs.
Elena is consistent through handover, objection, departure and tacos. Salas is
distinct from the archive witness. The later attendant is Omar, not Chano.

Nine corrective image calls were selected after visual inspection:

- Cover and handover: remove unsolicited literary slogans and advertising.
- Salas: distinguish his face from the archive witness.
- Fall, two edits: clarify Chano catching the technician's forearm, then remove
  real-company/agency branding that misidentified the transport staff.
- Waiting room: return the photograph to its mother-owner, not to Chano.
- Returns counter: remove an invented land-registry sign and promotional posters.
- Two Amealco scenes: place Q's right foot visibly on its support; the second
  also removes invented institutional mottos.

Every selected image was inspected at native resolution and again in the PDF.
The coat bag and service equipment are not the sealed archive deposit; no plate
puts the delivered module among the retained papers. The testimony remains
unseen. The administrative offices and future custody procedure are fictional,
not current-law illustrations. Background maps and architecture are illustrative,
not surveyed location records. No scene depicts a US crossing or a deathbed.

Final PNGs, exact prompts, reference paths, edit history, native dimensions and
SHA-256 values are recorded in
`output/illustrations/revised/issue-10/manifest.json`. All final assets are copied
into that project directory; original generated variants remain preserved.
No procedural editing of illustration rasters was used. Small color accents in
the source artwork are converted to neutral grayscale by the PDF pipeline.

## Edition and verification

4,422 words; 28 comic pages; fourteen plates including cover; thirteen continuous
two-column narrative pages plus publication-information back matter. Georgia
12.7/17.9917-point type. There are no forced interlude breaks or empty narrative
columns. Comic trim is 477 x 738 points. Text backgrounds are unpainted: cream
must come from paper stock. Plates reach comic trim, with separately typeset
captions in inset white strips. The cover title is set in two lines in its clear
upper area, without painting over the artwork.

The PDF skill's render-and-inspect workflow was applied to all 28 reading pages
and all fourteen A3 landscape sides. The A3 version is centered at actual size
for seven short-edge duplex sheets. Folding leaves an A4 carrier around the
smaller comic trim; trimming is separate. Automated checks confirm:

- Every source word occurs in exact order through the two columns.
- Narrative pages have no background rectangles, fills or images.
- Fourteen distinct approved native asset hashes match the current manifest.
- All actual A3 positions contain their reading page's text and decoded image
  data, with correct translation and trim clipping, not merely matching labels.
- Reading and A3 dimensions and zero reverse-page rotations match the specification.
- Fourteen PDF plates are lossless DeviceGray; five reading-font subsets are embedded.
- The manuscript, outline and existing Issues 1–9 PDFs are unchanged from baseline.

Proof hashes:

- Reading: `2d3f7728a2d36cce5fe698c015751f23373e3df6750d58577167484233a9b6f5`.
- A3: `99234dbc0273085e2f1807a6f52d663810ccb942308aa161176af6c77cac01be`.

Native artwork is 1024 x 1536, approximately 150 dpi at trim. The proofs are not
press masters; physical printer tray order, duplex-driver behavior, ink-on-stock
legibility and print resolution still require review. No print job was sent.
Twelve later illustrated issues, broader literary review and the updated Spanish
edition remain unfinished. The active goal is not complete.

## Reproduction notes

Development scripts, raw generation records and renders remain under `/tmp`:
`ingenious-issue10-art-selected.json`, `build_ingenious_issues_v2.py`,
`ingenious-issue10-finalize.py`, `qa_ingenious_issue1.py`,
`check-ingenious-issue10.py` and `ingenious-issue10-contacts.py`.
The RGB build is under `ingenious-issue10-rgb`; checked grayscale proofs, layout,
all reading/A3 renders and contact sheets are under `ingenious-issue10-final`.

Ghostscript's PDF writer used Gray/DeviceGray conversion, FlateEncode image
filters, disabled automatic lossy filters and disabled all image downsampling.
The grayscale reading PDF was then imposed, preserving the same decoded images
in the A3 version. Neither generation nor those checks establish literary grade.
