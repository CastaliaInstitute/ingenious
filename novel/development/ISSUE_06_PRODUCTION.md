# Issue 6: The Governor of the Model Town

## Scope and source

This pass illustrates current English Chapter Six. It does not revise the prose
or impose a new ending. The manuscript remains unchanged from `0f507260`; its
final line is **The Custodian put down his pen.** Finishing the shared book does
not require Q's destruction.

Chapter SHA-256:
`fa9380fe45bbcfab82191e13f00b0c58bb8a26bb4c259d4897353d362e4a037f`.

The accompanying `CHAPTER_06_FRESH_CONTEXT_REVIEW.md` reports four actual
inference calls, their differing responses and limits. The existing offer of
paid travel and Chano's money check are retained. An eloquent machine should
not turn another person's lost job into an opportunity for flattering prose.
This is not an A+ literary certification or an ask-faculty review.

## Edition specification

- Comic trim: 477 x 738 points, 6.625 x 10.25 inches.
- 2,802 printable narrative words; no source cuts or additions to fit.
- 20 pages: illustrated cover, nine two-column narrative pages, nine unique
  facing plates, and publication-information back page.
- Georgia 12.7/17.9917-point text. Final narrative columns use 575.73 and
  593.72 points. The chapter flows continuously through the text pages.
- Narrative backgrounds are unpainted. Cream is supplied by paper stock,
  not a printed tint or rasterized text panel.
- Full-bleed art at comic trim; captions separately typeset in inset white
  margin strips. The cover title occupies its reserved white upper field.
- A3 landscape: ten sides, five duplex sheets, centered at actual size.
  Short-edge duplex, all sides, no reverse-page rotation. Fold guides remain
  outside comic trim. Folding leaves an A4 carrier; trimming is separate.

## Facing scenes

| Narrative page | Plate page | Scene |
| --- | --- | --- |
| 2 | 3 | Chano's name on the personalized municipal display |
| 4 | 5 | Irma requests the household report while Chano studies the map |
| 6 | 7 | Chano reads his contract; Q closes the manuscript |
| 8 | 9 | Leticia identifies the last cleaning round |
| 10 | 11 | Q and Candelaria hold opposite ends of the measuring tape |
| 12 | 13 | The truck fills Maribel's jugs |
| 14 | 15 | Chano and Q compare two monthly totals with the ledger |
| 16 | 17 | Maribel retains the water demand; Leticia corrects the time |
| 18 | 19 | Q puts the tablet away after Chano loses the appointment |

The cover centers Chano in the ordinary five-caster padded office chair. The
contract plate uses a different, closer composition rather than repeating it.
Irma's short silver hair and glasses, Leticia's high dark bun and work clothes,
and Maribel's low ponytail and striped shirt distinguish the recurring women.
Leticia is not the earlier receptionist Lety; this Maribel is not automatically
the later corridor worker sharing her name. Reuse these identities in Chapter
Fourteen. Candelaria follows her Issue Five reference. The Custodian is absent
in person: an evening call does not put him in the office.

Santa Rita and its maps are fictional. The illustrations use contemporary
concrete public buildings, ordinary work clothing, a water truck and jugs,
not a colonial palace or Sancho's literal throne. The forest inspection retains
the earlier oyamel setting. Water delivery is a real local success in the story,
not a claim that the underlying shortage or land boundary has been resolved.

## Assets and corrections

`output/illustrations/revised/issue-06/manifest.json` records the exact facing
text, source blocks, nine scene anchors, full generation prompts, references,
selected hashes and individual visual-review notes. Ten selected PNGs are
saved beside it. The built-in image tool produced a unique composition for
each scene. A targeted edit moved the water stream into the open jug's neck;
the first image incorrectly poured onto its shoulder. Failed service requests
were retried only for missing scenes. All cached originals remain intact.

The Issue Fourteen plan now references Irma, Leticia, Maribel and the chair from
this issue. It remains a plan, not an approved illustrated Issue Fourteen.
Its remote Q must not be placed in Santa Rita simply because he appears in
these visual references.

All selected PNGs are 1024 x 1536 RGB originals, approximately 149.85 dpi after
full-bleed placement. They were copied without procedural image editing.
Ghostscript converted the reading PDF only to grayscale, with no downsampling
and explicit lossless Flate image filters. The final PDF contains ten
DeviceGray images, not JPEG recompressions or newly invented 300-dpi detail.
The A3 file was imposed from this grayscale reading PDF.

## Verification and delivery

Independent PDF extraction verifies all 2,802 narrative words exactly once in
source order. No narrative page contains a painted fill, image or background
rectangle. All five reading-PDF font subsets are embedded. Comic/A3 dimensions,
zero page rotation and all five duplex sheet pairs pass:

`20,1 / 2,19; 18,3 / 4,17; 16,5 / 6,15; 14,7 / 8,13; 12,9 / 10,11`.

All twenty reading-page renders were visually inspected, including every
caption, title and final column. Separate checks covered the A3 outside cover,
first reverse and center spread. The other A3 sides received structural pair
and dimension checks. No physical print, fold or printer-tray-order test was
performed, and no print job was sent.

All twenty-two current manifests match fresh chapter and pagination plans.
Issues 1-6 now have unique, inspected, hash-bound art; Issues 7-22 remain planned.
The manuscript and all existing Issue 1-5 reading/A3 PDFs are byte-identical to
`0f507260`. The living-Q ending is unchanged.

- Reading: `output/pdf/ingenious-issue-06-revised-en-bw.pdf`.
  SHA-256: `3d71ca3fb53f433ac9edee934d440541716f433b9e98f02a6914388811297db9`.
- A3: `output/pdf/ingenious-issue-06-revised-en-bw-a3.pdf`.
  SHA-256: `7ff5b962450f43261c4d27a09da7fcb860659031196c1b7305ba371e31ddd57f`.

Development and test artifacts remain under `/tmp`: the shared
`build_ingenious_issues_v2.py` and `qa_ingenious_issue1.py`,
`check-ingenious-issue06-final.py`, `ingenious-issue06-contacts.py`,
`ingenious-issue06-plans`, and `ingenious-issue06-final` including page renders
and `qa-result.json`. The text-only and cover-type trials are not deliverables.
These are revision proofs, not press masters. Native resolution and ink-on-stock
reproduction still need press review. The larger revision goal remains active.
