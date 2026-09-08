# Issue 4: The Intelligence of the Trending Hour

## Scope and source

This production pass illustrates the current English Chapter Four and both
interludes without changing the manuscript. Q negotiates an appearance, enjoys
an audience and faces the misuse of his words. Nora and her grandmother have
their own conversation; Don Hilario's wage dispute and memory of his brother
remain his, not material Q acquires. The final plate shows useful arithmetic,
not the later courtroom's interpretation of it.

The chapter SHA-256 is
`2763808943e7dae932463cf7100e2a6791159c54d011c56764e1d98ee0c48700`.
The complete manuscript is byte-identical to the source at `318b1852`.
This is an illustrated revision proof, not a new whole-book literary assessment.

## Edition specification

- Complete English chapter and interludes: 5,211 printable narrative words.
- Comic trim: 477 x 738 points (6.625 x 10.25 inches).
- 32 pages: illustrated cover, fifteen continuous two-column narrative pages,
  fifteen facing plates, and a publication-information back page.
- Georgia 12.2/17.2833-point text. The prior 12-point plan left the final second
  column empty; the revised setting uses 587.63 and 483.93 points in the final
  columns. No source text was cut or added to reach the page count.
- Interlude headings remain in the text flow, beginning on pages 14 and 22.
  No forced page breaks between chapter sections.
- Unpainted white narrative pages. Cream is supplied by paper, not ink.
- Full-bleed monochrome images at comic trim, with separately typeset captions
  in inset white margin strips. The cover title uses two lines so its final
  letters do not run into the curtain; the original single-line proof failed
  that visual check.
- A3 landscape: sixteen sides, eight duplex sheets, centered at actual size.
  Print all sides, short-edge duplex; there is no reverse-side PDF rotation.
  Fold ticks and instructions are outside trim. Folding leaves an A4 carrier
  around the smaller comic page, so trimming is still a separate operation.

## Facing illustrations

| Narrative page | Plate page | Selected scene |
| --- | --- | --- |
| 2 | 3 | Chano inspects Mar's offered sponsor jacket |
| 4 | 5 | Van window, cat and Chano's missing musical note |
| 6 | 7 | Estela moves the empty chair away from a cable |
| 8 | 9 | Mar forwards a removal request while Beto asks for numbers |
| 10 | 11 | Q asks who replaces the candle in the mine niche |
| 12 | 13 | Chano writes his own contract margin |
| 14 | 15 | Phones, technician, geometric ceiling and star chandelier |
| 16 | 17 | Estela interrupts Q's qualified answer |
| 18 | 19 | Nora watches the clips on the bus home |
| 20 | 21 | Nora's grandmother points to the dry faucet |
| 22 | 23 | Hilario and the entrance's souvenir helmets |
| 24 | 25 | Chano inspects the old lever; separate working controls |
| 26 | 27 | Hilario points to the disputed shift date |
| 28 | 29 | A remembered lunch joke; Q turns the lamp away |
| 30 | 31 | Chano copies selected figures and Q checks the second sum |

The cover has a distinct over-Q's-shoulder view from the wing, not a repeat of
Estela moving the chair. Q's established head, circular ear mechanism, narrow
neck and articulated frame anchor the set. His old coat appears before the
wardrobe change; subsequent plates use the fitted sponsor jacket. Chano, Mar,
Beto, Estela, Nora and Hilario have explicit recurring references. The Custodian
does not physically appear in these scenes; his call and written advice do not
justify adding him to the room. Nora's two plates contain no Q.

The [Guanajuato cultural authority's theater description](https://cultura.guanajuato.gob.mx/index.php/teatro-juarez/)
and page 2 of its [venue catalog](https://cultura.guanajuato.gob.mx/wp-content/uploads/2025/03/cata%CC%81logo_espacios_cultura_mar25_.pdf)
inform the geometric ceiling, star chandelier and iron horseshoe balconies.
The event staging is fictional and the drawings are not measured architectural
reconstructions. The mines, records, other city views and incidents are invented,
not verified depictions of a specific tourist mine or actual payroll.

## Assets, prompts and corrections

`output/illustrations/revised/issue-04/manifest.json` contains the exact facing
text, block IDs, scene anchors, reference images, full generation and edit
prompts, review notes and selected asset hashes. All sixteen selected PNGs are
saved beside it. Generation used the built-in image tool, one scene per request;
no command-line image service or procedural replacement art was used.

The first cover repeated the chair-moving pose and was replaced with the wing
view. Targeted edits corrected Nora's phone facing the viewer, removed
inappropriate figure sculpture from the cover's theater background, and gave
Chano rather than Hilario the action at the old lever. The duplicate Chano in
that lift image was also removed. Original generated files remain in the image
cache. `plate-09.png` is the retained, unused first phone variant; the selected
asset is `plate-09-v2.png`.

Each selected image is 1024 x 1536 pixels, about 149.85 dpi after full-bleed
placement. Original RGB PNGs are unchanged. PDF prepress conversion uses
Ghostscript `ColorConversionStrategy=Gray`, no image downsampling,
`AutoFilterGrayImages=false`, `GrayImageFilter=/FlateEncode`, and equivalent
color-filter flags. The final PDFs contain DeviceGray images with lossless
compression, not JPEG recompression or artificially claimed 300-dpi detail.

## Verification and outputs

Independent extraction confirms all 5,211 narrative words once and in source
order; no raster, background rectangle or painted fill occurs on narrative
pages. All sixteen illustration pages contain one DeviceGray raster. Comic and
A3 dimensions, zero rotation and every booklet pair pass structural checks:

`32,1 / 2,31; 30,3 / 4,29; 28,5 / 6,27; 26,7 / 8,25;`
`24,9 / 10,23; 22,11 / 12,21; 20,13 / 14,19; 18,15 / 16,17`.

All 32 reading pages received rendered visual review, including captions,
interlude flow and the last two narrative columns. The corrected cover and
final A3 cover, first reverse and center spread were separately inspected.
After the cover-only typography fix, all 31 interior/back page renders were
pixel-identical to the reviewed version. All five font subsets are embedded.
The other A3 sides receive pair/size checks, not a claim of physical folding.
All 22 current issue manifests match fresh pagination plans; Issues 1-4 have
reviewed, hash-bound art and Issues 5-22 retain planned status.

- Reading: `output/pdf/ingenious-issue-04-revised-en-bw.pdf`
  SHA-256: `1ac075f79de5efba11b11a535c81042c731373805e72b95837ce627cd8cf688f`.
- A3: `output/pdf/ingenious-issue-04-revised-en-bw-a3.pdf`
  SHA-256: `d9a5abc86fb48c232f872931601d8783a2e011df647930cc260e82499ba50db8`.

The builder and QA scripts remain under `/tmp`: `build_ingenious_issues_v2.py`,
`qa_ingenious_issue1.py`, `check-ingenious-issue04-bindings.py`, and
`ingenious-issue04-contacts.py`. The builder's optional cover `title_lines`
preserves the exact book title when fitting a narrower quiet area; other issues
retain their existing title layout.

## Remaining limitations

Fine generated mechanical and facial details still require a final series-wide
art-continuity pass. Native raster resolution, ink density, paper opacity,
actual printer tray order and duplex-driver behavior remain unverified. No print
job was sent and no A+ press-master claim is made. Eighteen chapter issues still
need revised illustrated builds; broader pacing review, further scene tests,
current full-book PDFs and the Spanish revision remain open under the active goal.
