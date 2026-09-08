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

- The subsequent paid-companion continuity pass adds exactly eighty words at
  the motel: Chano and Q agree tomorrow's rate separately from food and fares,
  check it against Q's card limit, and leave further days subject to agreement.
  See `PAID_COMPANION_CONTINUITY.md`. This anchors the agreement later recalled
  in Chapters Six and Sixteen without inventing a numerical running balance.
- English Chapter Two and its interludes: 4,480 rendered narrative words.
- Comic trim: 477 x 738 points, or 6.625 x 10.25 inches.
- 32 pages: cover, fifteen continuous narrative pages, fifteen facing plates,
  and a publication-information back page.
- Georgia 13.3 / 18.8417-point body text in two columns. Paragraphs flow between
  columns and narrative pages; interludes begin within pages 14, 24 and 30.
- Narrative backgrounds are unpainted. Cream must come from the paper stock.
- Sixteen unique monochrome illustrations including the cover, full bleed at
  comic trim, with separately typeset captions in inset white strips.
- A3 landscape carrier: sixteen sides, eight duplex sheets, centered actual-size
  comic spreads. Short-edge duplex; no reverse-side PDF rotation. Fold ticks and
  sheet labels sit outside trim. Folding gives an A4-size carrier around the
  smaller comic trim; trimming is a separate operation.

| Narrative page | Facing plate page | Scene |
| --- | --- | --- |
| 2 | 3 | Chano's dismissal; wedding photograph and receipt in his wallet |
| 4 | 5 | The closed gate's satisfied diagram |
| 6 | 7 | Q photographs the dashboard through the closed cab window |
| 8 | 9 | Lety examines two damaged cartons |
| 10 | 11 | Lety returns the bags and names the prior trailer complaint |
| 12 | 13 | Motel receipt and tomorrow's pay agreement |
| 14 | 15 | Q reads the public event notice |
| 16 | 17 | Concha, coffee and company |
| 18 | 19 | Chano crosses out his own Dulcinea entry |
| 20 | 21 | Celia keeps the register closed; camera confrontation |
| 22 | 23 | Celia hands Chano the torn register page |
| 24 | 25 | Hilario disputes the price of ice with the guard |
| 26 | 27 | Cash, failed reader and retained receipt |
| 28 | 29 | Hilario records Q for his wife; a crate obscures Chano |
| 30 | 31 | Earlier floor-scrubber mishap; coat hem, not a shoelace |

Page 26 contains the failed reader and cash transaction. Page 28 distinguishes
Hilario's original recording from the later licensing visit. The closed-register
plate depicts a scene spanning pages 20 and 22: Celia closes the book and Q
stands beside her on page 20; Chano blocks the camera on page 22.

## Assets and review limits

`output/illustrations/revised/issue-02/manifest.json` records the chapter hash,
exact facing text, source block IDs, captions, all asset hashes, exact generation
and edit prompts, and revision-proof approval scope. All sixteen selected PNGs
are saved beside the manifest. Built-in image generation produced distinct
scenes, using the Issue 1 cover for Q and Issue 3 plate 6 for Chano. Issue 2 plates
4, 7 and 11 establish Lety, Celia and Hilario respectively.

The reflow retains thirteen existing images and adds three built-in-generated
plates: `supplement-gate.png`, `supplement-pay.png`, and `supplement-video.png`.
The video image needed one corrective edit so the phone preview, like the larger
scene, shows Chano's face partly obscured by the crate. Both attempts are recorded
in the manifest. The old emergency-stop `plate-03.png` remains on disk but is not
selected: the stop and damaged cartons now share one narrative page. Filenames
are historical asset names; current page assignments come from the manifest.

The first truck-window edit failed to remove an unwanted woman's reflection.
The second removed the face reflections from the glass while preserving the
actual Q and Chano outside the cab. The manifest records both attempts rather
than describing the first as successful. Original generated files were retained.

All sixteen selected assets are 1024 x 1536 pixels: approximately 149.85 dpi at full-bleed
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

The independent PDF checker confirms all 4,480 narrative words exactly once in
source order, no fills/images/background rectangles on narrative pages, sixteen
DeviceGray plate images, no lossy JPEG image encoding, correct comic and A3 page
dimensions, zero page rotation and the following nested booklet pairs:

`32,1 / 2,31; 30,3 / 4,29; 28,5 / 6,27; 26,7 / 8,25; 24,9 / 10,23; 22,11 / 12,21; 20,13 / 14,19; 18,15 / 16,17`.

All 32 trim pages were rendered and visually inspected, including all fifteen
narrative pages, all sixteen images and captions, and the colophon. No clipped
text or caption overlap with faces/hands was found. The A3 cover, first reverse
and central spread were also rendered and inspected. Remaining A3 sides receive
structural pair/size checks, not a claim of physical folding verification.

- Reading: `output/pdf/ingenious-issue-02-revised-en-bw.pdf`
  SHA-256: `e294880f68a8206e62fadf5624b6e1273e220c00e30fb3cb46817de06de93ad5`.
- A3: `output/pdf/ingenious-issue-02-revised-en-bw-a3.pdf`
  SHA-256: `85d1aa9eb8742047cdcd5bac8c5d8f87b362c6e8483f2547228c3b79215a4e65`.

Development files and render outputs remain under `/tmp`. The build uses
`build_ingenious_issues_v2.py`; independent checking uses the variable-page-count
`qa_ingenious_issue1.py`. All 22 current pagination plans pass the builder's
rendered-text/source-order comparison. All 22 manifests pass exact facing-text
and chapter-hash checks; Issues 1-6 have unique approved selected art. All five
PDF fonts are embedded. The exact eighty-word addition is the only manuscript
change from `2e9b26ed`; the other 21 chapters, ending, all fourteen earlier Issue
Two PNGs and Issues 1/3/4/5/6 PDFs are unchanged. Earlier Issue Two PDFs remain
recoverable from Git history.

## Remaining scope

Sixteen chapter issues still need their revised illustrated builds. Full-book
PDFs, the Spanish revision, cross-book voice review and independent scene tests
remain unfinished. This production check does not establish a literary grade
or close the active two-book revision goal. Q's ordinary life beyond the
Custodian's final sentence remains the ending principle.
