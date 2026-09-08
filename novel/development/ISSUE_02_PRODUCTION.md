# Issue 2: The First Sally

## Current revision

Q meets the dismissed freight worker Chano, obtains permission to enter reception,
and makes a precautionary stop with an obstructed view. Lety's existing complaint
about the trailer survives the supposed rescue story. At the motel, Celia refuses
Castalia's camera access; at the roadside, Hilario has a business rather than a
supporting role to sell. The floor-scrubber interlude returns to an earlier moment.

The production read corrected premature video knowledge: Hilario now asks about
the stopped bay, and Q asks what the guard has told him. Q does not critique an
edit he has not yet seen. This change adds twelve rendered words to the earlier
layout plan. The complete chapter and all three interludes remain present.

## Edition specification

- English Chapter Two and its interludes: 4,400 rendered narrative words.
- Comic trim: 477 x 738 points, or 6.625 x 10.25 inches.
- 28 pages: cover, thirteen continuous narrative pages, thirteen facing plates,
  and a publication-information back page.
- Georgia 12.4 / 17.5667-point body text in two columns. Paragraphs flow between
  columns and narrative pages; interludes begin within pages 12, 20 and 26.
- Narrative backgrounds are unpainted. Cream must come from the paper stock.
- Fourteen unique monochrome illustrations including the cover, full bleed at
  comic trim, with separately typeset captions in inset white strips.
- A3 landscape carrier: fourteen sides, seven duplex sheets, centered actual-size
  comic spreads. Short-edge duplex; no reverse-side PDF rotation. Fold ticks and
  sheet labels sit outside trim. Folding gives an A4-size carrier around the
  smaller comic trim; trimming is a separate operation.

| Narrative page | Facing plate page | Scene |
| --- | --- | --- |
| 2 | 3 | Chano's dismissal; wedding photograph and receipt in his wallet |
| 4 | 5 | Q photographs the dashboard through the closed cab window |
| 6 | 7 | Obstructed walk and local emergency stop |
| 8 | 9 | Lety examines two damaged cartons |
| 10 | 11 | Lety returns the bags and names the prior trailer complaint |
| 12 | 13 | Q reads the public event notice |
| 14 | 15 | Concha, coffee and company |
| 16 | 17 | Chano crosses out his own Dulcinea entry |
| 18 | 19 | Celia keeps the register closed; Chano blocks the camera |
| 20 | 21 | Celia hands Chano the torn register page |
| 22 | 23 | Hilario disputes the price of ice with the guard |
| 24 | 25 | Cash, failed reader and retained receipt |
| 26 | 27 | Earlier floor-scrubber mishap; coat hem, not a shoelace |

The cash transaction spans the preceding and facing narrative pages. Page 24
continues the purchase, refers to the failed reader, and records Q keeping the
receipt; the plate does not represent the later licensing visit.

## Assets and review limits

`output/illustrations/revised/issue-02/manifest.json` records the chapter hash,
exact facing text, source block IDs, captions, all asset hashes, exact generation
and edit prompts, and revision-proof approval scope. All fourteen selected PNGs
are saved beside the manifest. Built-in image generation produced distinct
scenes, using the Issue 1 cover for Q and Issue 3 plate 6 for Chano. Issue 2 plates
4, 7 and 11 establish Lety, Celia and Hilario respectively.

The first truck-window edit failed to remove an unwanted woman's reflection.
The second removed the face reflections from the glass while preserving the
actual Q and Chano outside the cab. The manifest records both attempts rather
than describing the first as successful. Original generated files were retained.

All fourteen assets are 1024 x 1536 pixels: approximately 149.85 dpi at full-bleed
trim. Final PDF images use DeviceGray and lossless Flate compression without
downsampling. This does not create 300-dpi detail. The recurring Q silhouette,
head construction and breastplate are recognizable, but fine facial, coat-tear
and costume details vary between generated views. Incidental skylines and
buildings are fictional illustration, not verified views of particular places.
These limitations remain for a final art-continuity and press-resolution pass.

This is a revision proof, not an A+ press master. Physical ink density, stock
opacity, actual printer output order and driver duplex settings have not been
verified. No print job was sent.

## Verification

The independent PDF checker confirms all 4,400 narrative words exactly once in
source order, no fills/images/background rectangles on narrative pages, fourteen
DeviceGray plate images, no lossy JPEG image encoding, correct comic and A3 page
dimensions, zero page rotation and the following nested booklet pairs:

`28,1 / 2,27; 26,3 / 4,25; 24,5 / 6,23; 22,7 / 8,21; 20,9 / 10,19; 18,11 / 12,17; 16,13 / 14,15`.

All 28 trim pages were rendered and visually inspected, including all thirteen
narrative pages, all fourteen images and captions, and the colophon. No clipped
text or caption overlap with faces/hands was found. The A3 cover, first reverse
and central spread were also rendered and inspected. Remaining A3 sides receive
structural pair/size checks, not a claim of physical folding verification.

- Reading: `output/pdf/ingenious-issue-02-revised-en-bw.pdf`
  SHA-256: `2be232b911bdbb4fa24b0973a501ddcd053a27cade63dc1914a89240a9a87b6c`.
- A3: `output/pdf/ingenious-issue-02-revised-en-bw-a3.pdf`
  SHA-256: `36f2823bab90e66ac2388d78154fe7fefeb721fd3f76f9632e1924cb260cbf02`.

Development files and render outputs remain under `/tmp`. The build uses
`build_ingenious_issues_v2.py`; independent checking uses the variable-page-count
`qa_ingenious_issue1.py`. All 22 current pagination plans pass the builder's
rendered-text/source-order comparison. The three completed issue manifests pass
exact facing-text and chapter-hash checks. Issues 1 and 3 were not rebuilt here.

## Remaining scope

Nineteen chapter issues still need their revised illustrated builds. Full-book
PDFs, the Spanish revision, cross-book voice review and independent scene tests
remain unfinished. This production check does not establish a literary grade
or close the active two-book revision goal. Q's ordinary life beyond the
Custodian's final sentence remains the ending principle.
