# Issue 5: The Butterflies Have No General

## Scope and source

This pass illustrates the current English Chapter Five and its three interludes.
It does not revise the prose or impose a new ending. The complete manuscript is
byte-identical to `fe899220`; its final line remains **The Custodian put down his
pen.** Q need not die for the writing to stop.

Chapter SHA-256:
`346b6c0d6152d45e12d21660a0feaaf8c9e8d8e4c7fcf4201bf7fab5115268a7`.
All existing Issue 1-4 reading and A3 PDFs are also byte-identical to that commit.
This is a bounded illustrated revision proof, not a new A+ literary assessment.

## Edition specification

- 7,202 printable narrative words, preserved once in source order.
- Comic trim: 477 x 738 points, or 6.625 x 10.25 inches.
- 44 pages: illustrated cover, twenty-one continuous two-column narrative pages,
  twenty-one unique facing plates, and a publication-information back page.
- Georgia 12.45/17.6375-point text. Final narrative columns use 599.67 and
  458.66 points. No source text was cut, added or repeated to reach the page count.
- Interlude headings flow on pages 20, 26 and 34; the final appointment section
  begins in the second column of page 42. No forced section page breaks.
- Narrative backgrounds are unpainted white. Cream comes from the paper stock,
  not a tinted page rectangle or rasterized text.
- Full-bleed monochrome art at comic trim, with separately typeset captions in
  inset white margin strips. No caption is baked into the selected PNG.
- The cover title uses two lines, with its center at x=273 points. Both the
  single-line title and the page-centered two-line trial overlapped dark branches;
  shifting the type into the open sky avoids painting over the forest.
- A3 landscape: twenty-two sides, eleven duplex sheets, centered at actual size.
  Short-edge duplex, all sides, no PDF reverse rotation. Fold ticks and guide
  text remain outside trim. Folding produces an A4 carrier around the smaller
  comic page; trimming remains a separate step.

## Facing plates

| Narrative page | Plate page | Scene |
| --- | --- | --- |
| 2 | 3 | Beto's artificial butterfly over motel breakfast |
| 4 | 5 | Q makes room for a child beneath the monarch bough |
| 6 | 7 | Candelaria's young trees on the burned slope |
| 8 | 9 | Coat, bucket and wire left loose enough for growth |
| 10 | 11 | Schoolgirl remembers her grandmother's shoes |
| 12 | 13 | Two maps give different distances to the spring |
| 14 | 15 | Elder and secretary check the disputed boundary |
| 16 | 17 | Q and the young man fold the borrowed canvas |
| 18 | 19 | Lidia and her mother privately preview the report |
| 20 | 21 | Director mutes the butterfly animation |
| 22 | 23 | Mother checks the time while the assistant prepares paperwork |
| 24 | 25 | Q writes the changed removal request |
| 26 | 27 | Family leaves; Q holds the door and Chano checks the bus |
| 28 | 29 | Q holds the market tarp pole in the rain |
| 30 | 31 | The honey seller's customers have moved indoors |
| 32 | 33 | Music interrupts table-carrying beneath the store stairs |
| 34 | 35 | Tere, the transmitter and three notebooks |
| 36 | 37 | Recording stops for the private call |
| 38 | 39 | Football complaints have become a supposed land dispute |
| 40 | 41 | Q stays to hear the uncle's prerecorded song |
| 42 | 43 | Chano considers shaving for himself and the photograph |

The cover has its own rear-quarter forest composition, not a duplicate of an
interior. Q keeps his segmented oval head, circular ear mechanisms, slender
articulated body and fitted sponsor jacket. Chano, Beto, Candelaria, the ledger
keeper, Lidia and her mother, the student partner and Tere have explicit visual
references. The watering girl, grieving schoolgirl and Lidia are distinct people.
The director is a woman; the Custodian is male but does not physically appear
in this chapter. His evening call does not justify placing him in the room.

The reserve, office, station and town views are fictional illustrations, not
verified reconstructions of named properties. The assembly and reserve-office
views retain highland fir surroundings; the later market and radio sequences
take place in town. The projected needs map is an invented classification
graphic, not a geographic claim or a verified map of an actual conflict.

## Assets and corrections

`output/illustrations/revised/issue-05/manifest.json` records exact facing text,
source block IDs, scene anchors, references, full generation and edit prompts,
selected asset hashes and visual-review notes. All twenty-two selected PNGs are
saved beside it. The built-in image tool generated one original per requested
scene. Four targeted edits moved the monarch to Q's jacket emblem and corrected
the assembly, private-preview and handwritten-request backgrounds. Original
cached images remain intact. No command-line image service or procedural
replacement illustration was used.

Each selected PNG is 1024 x 1536 pixels, approximately 149.85 dpi after full-bleed
placement. Native PNGs remain unchanged. PDF-only Ghostscript conversion uses
`ColorConversionStrategy=Gray`, no downsampling, `AutoFilterGrayImages=false`,
`GrayImageFilter=/FlateEncode`, and equivalent color-filter flags. The final
reading PDF contains twenty-two DeviceGray images with lossless compression,
not JPEG recompression or a claim of newly created 300-dpi detail. The A3 PDF
was imposed from that grayscale reading PDF.

## Verification and delivery

Independent PDF extraction verifies all 7,202 narrative words in source order,
with no raster, background rectangle or painted fill on any narrative page.
All five reading-PDF font subsets are embedded. Comic/A3 dimensions, zero A3
rotation and all eleven sheet pairs pass:

`44,1 / 2,43; 42,3 / 4,41; 40,5 / 6,39; 38,7 / 8,37;`
`36,9 / 10,35; 34,11 / 12,33; 32,13 / 14,31; 30,15 / 16,29;`
`28,17 / 18,27; 26,19 / 20,25; 24,21 / 22,23`.

All 44 reading-page renders were visually inspected, including every caption,
the cover typography, section transitions and final columns. The A3 cover,
first reverse and center spread received separate visual review; the remaining
A3 sides received structural pair/size checks. No physical printing or folding
was performed, and no printer job was sent.

All twenty-two current issue manifests match fresh chapter/pagination plans.
Issues 1-5 now have unique, inspected, hash-bound art; Issues 6-22 remain planned.

- Reading: `output/pdf/ingenious-issue-05-revised-en-bw.pdf`.
  SHA-256: `1912c0f1bc1a095427affe3a326ce93b12b797b2346dd5cfdc2dd2518729d761`.
- A3: `output/pdf/ingenious-issue-05-revised-en-bw-a3.pdf`.
  SHA-256: `1805c6488f74b5ad7a325ad399731ecb4cc17d097d36a56eb92904b030460dba`.

The builder, comparison scripts, text-only trials and rendered QA sheets remain
under `/tmp`: `build_ingenious_issues_v2.py`, `check-ingenious-issue05-final.py`,
`qa_ingenious_issue1.py`, `ingenious-issue05-contacts.py`, and the
`ingenious-issue05-final` directory. The builder's optional cover
`title_center_x_pt` reads the value recorded in the manifest; other covers retain
their previous default. These are revision proofs: native resolution and actual
ink-on-stock reproduction still need press review. The larger goal stays active.
