# Issue Eight: The Giants of the Isthmus

## Editorial scope

Baseline: `1afe0adc`. The complete chapter, outline entry, Q design and gate
simulation revision were reread before illustration. Chapter Sixteen's two
accounts retain Q inside the bay and attribute the photographer's later route
to the staff report. Chapter Seventeen's return uses the designated path.

One source correction changes "nine letters" to "ten letters": *accomplice*
contains ten letters. No new plot event is introduced. The living ending remains
"The Custodian put down his pen."

Q recognizes turbines as suppliers to his archive through the grid. His practical
request to the guard succeeds; the photographer seeks his own composition.
The later proposal about community authorization is fluent but inadequate:
it conceals which body may decide. Competence and fallibility coexist without
making an archaic robot misunderstand machinery or ordinary speech.

The radio exchange, fan, coffee and improved shoulder provide comic relief
without resolving the detentions. Bixha has work before and after Q's arrival.
Permissions and recordkeeping remain frequent subjects across the book; this
chapter-level check does not establish whole-book rhythm or an A+ grade. No
fresh independent simulation was run in this production pass. The earlier
bounded probes and authored consequences remain documented in
`GATE_SIMULATION_REVISION.md`.

## Cultural grounding

[Radio Educación's catalog](https://catalogoradioeducacion.cultura.gob.mx/programas/musica-del-istmo-de-tehuantepec/)
places *La Sandunga* in its Isthmus music program. The
[Culture Secretariat's band recording catalog](https://cid-albertobeltran.cultura.gob.mx/catalogo-en-linea-fonoteca/sones-de-oaxaca/)
lists a Tehuantepec band's performance, supporting the brass-part joke without
reproducing lyrics or a recording. The
[Energy Secretariat's regional assessment](https://www.gob.mx/sener/articulos/evaluacion-ambiental-y-social-estrategica-para-el-desarrollo-eolico-ease)
establishes the regional wind-development context, not the truth of the novel's
invented company or allegations. The site and access plan are fictional.

The radio plate's generic triangular chips were flagged for replacement with
round perforated Isthmus totopos. Their shape is described in an
[Oaxaca legislative document](https://www.congresooaxaca.gob.mx/docs66.congresooaxaca.gob.mx/gaceta/20251209a/11.pdf).
Only that food detail is used here, not the document's broader historical claims.

## Edition and verification

Verified layout: 2,671 words, 16 comic pages, eight unique plates including
the cover, seven continuous two-column narrative pages, and back matter.
Georgia 12/17-point type. A3 landscape: eight sides, four duplex sheets,
actual size, short-edge flip. Comic trim is 477 x 738 points. The A3 carrier
folds to A4 around the smaller comic trim; trimming is separate. Text backgrounds
remain unpainted, with cream supplied by stock. Full-bleed plates have separately
typeset inset white caption strips.

Eight original images and four corrective edits were made with built-in image
generation. All selected native PNGs were visually inspected. Corrections close
the gate in the arrival scene, send the sack-carrying woman toward the plots
while Q addresses the guard, separate the bus parking from the visitor bay on
the sketch, remove an invented photograph from the extract, and replace generic
chips with round perforated totopos. The source-bound manifest records exact
prompts, references, selected files and hashes. No procedural image editing was
used; grayscale conversion happened only in the PDF pipeline.

All sixteen final reading pages and all eight final A3 sides were rendered and
visually checked. Independent checks establish exact source-word order, no
painted text backgrounds, eight distinct lossless DeviceGray images, trim/A3
dimensions, zero reverse rotations and five embedded reading-font subsets.
The expanded imposition check compares each actual slot's text and decoded
image data with its source page, checks its translation, and verifies the trim
clipping path. A first diagnostic counted raw full-bleed image extents across
the neighboring slot; inspection confirmed that the PDF clips them at trim.
The corrected diagnostic explicitly verifies that clip before assigning images
by center. No PDF change was needed for that diagnostic correction.

All source changes are limited to the one-word count correction. The outline,
other twenty-one chapters and Issues 1-7 PDFs remain unchanged from baseline.
Proof SHA-256 values:

- Reading: `b8a914a9196fb432d436c883e85d643d165ec023dcf0096a015b3b94a2f18fbe`
- A3: `82609cecb5830f14197abcae2c06d7697947616d5099e064fc02ae159d09ca97`

The artwork is native 1024 x 1536, approximately 150 dpi at comic trim. These
are revision proofs, not press masters. Fine generated details and the fictional
site sketch are not surveyed or documentary evidence. Physical duplex behavior,
ink-on-stock legibility and print resolution still need review. No print job
has been sent. Fourteen later illustrated issues and the broader revision goal
remain open. Scripts, tests and renders stay in `/tmp`.
