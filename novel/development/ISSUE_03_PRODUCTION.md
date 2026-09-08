# Issue 3: Dulcinea Is Not Available

## Current revision

Q asks a real question, explains his writing purpose, accepts the public summary
and yields. An audience member supplies the Dulcinea comparison. Q rejects it,
then lets Lucía answer the follow-up herself. She returns the room to a school
crossing; the camera stays on him. The Chapter 4 interview and Chapter 18 child
conversation now recall that encounter, not the discarded unsolicited proposal.
Exercise 11 in `Q_SCENE_EXERCISES.md` records the author-run alternative and its
limits. There has been no independent fresh-context behavioral validation.

## Edition specification

- English Chapter Three and its interlude, complete: 3,219 rendered narrative words.
- Comic trim: 477 x 738 points (6.625 x 10.25 inches).
- 20 pages: cover, nine continuous narrative pages, nine facing plates, colophon.
- Georgia 12/17-point text in two columns; paragraphs flow across columns and
  narrative pages. The interlude begins within page 14, not on a forced new page.
- Unpainted white text pages. Cream comes from stock, not a printed background.
- Ten unique monochrome illustrations including the cover, full bleed at comic
  trim, with separately typeset captions in inset white strips.
- A3 landscape carrier: ten sides, five duplex sheets, centered at actual size.
  Short-edge duplex, no reverse-side PDF rotation. Folding leaves an A4-size
  carrier around the smaller comic trim; trimming remains a separate operation.

| Narrative page | Facing plate | Scene |
| --- | --- | --- |
| 2 | 3 | Q opens the bus window |
| 4 | 5 | Lucía and the engineer mark the pitch |
| 6 | 7 | Taco, parking meter and threatened phone extension |
| 8 | 9 | Lucía takes the microphone; Q yields |
| 10 | 11 | Livestream keeps Q, excludes the map |
| 12 | 13 | Chano carries the departing woman's bag |
| 14 | 15 | Araceli checks signature and thumbprint with Don Roque |
| 16 | 17 | A broken cookie after the missed lunch |
| 18 | 19 | The Custodian calls again |

The cover establishes Lucía's appearance at the warehouse. The Issue 1 cover
remains Q's and the male Custodian's identity reference. Plate 7 establishes
Araceli and Don Roque for plate 8. Incidental architectural views and maps are
fictional illustration, not geographically verified documentation. The map
discussion plate includes other residents around the named questioner's map.

## Assets and verification

`output/illustrations/revised/issue-03/manifest.json` holds exact facing text,
source block IDs, chapter hash, captions, asset hashes, generation prompts, and
approval limits. Built-in image generation supplied ten separate scenes. A
targeted edit removed invented slogans and labels from the engineer plate.
Every selected asset is saved in that directory, not merely in a generation cache.

All ten assets are 1024 x 1536 pixels, about 149.85 dpi at full-bleed trim. The
grayscale PDF uses lossless Flate image compression without downsampling. Native
detail has not been represented as 300-dpi detail. These are revision proofs,
not A+ press masters. Physical ink density, paper opacity, and printer feed order
remain unverified; no print job was sent.

The independent PDF checker confirms all 3,219 words once in source order, no
fills/images/background rectangles on narrative pages, ten DeviceGray plates,
correct trim/A3 dimensions, zero rotation and the following booklet pairs:

`20,1 / 2,19; 18,3 / 4,17; 16,5 / 6,15; 14,7 / 8,13; 12,9 / 10,11`.

Rendered review covers the narrative flow, all ten illustrated pages and captions,
the colophon, and the A3 cover, first reverse and central spread. No text clipping
or caption overlap was found. Other A3 sides receive structural pair/size checks,
not a claim of a physical folding test.

- Reading: `output/pdf/ingenious-issue-03-revised-en-bw.pdf`
  SHA-256: `1993ffebd785cd610f8aeaad29ad36c3b6a31af99b098ce9a61f0111ca86a39b`.
- A3: `output/pdf/ingenious-issue-03-revised-en-bw-a3.pdf`
  SHA-256: `9f60b703affbd13a8626af3205828d2353e1845c3d0a4946d1d8f77bf425064a`.

Development tools remain under `/tmp`: `build_ingenious_issues_v2.py` and the
now-variable-page-count `qa_ingenious_issue1.py`. The production method and
lossless grayscale flags are also recorded in `ISSUE_01_PRODUCTION.md`.

## Remaining scope

Issue 1 remains unchanged. Issue 2 has planned plates, not a completed new
illustrated PDF. The other chapter issues, full-book PDFs, Spanish revision,
cross-book voice review and independent scene tests remain unfinished. Finishing
this issue does not establish completion or an A+ grade for the two-book project.
