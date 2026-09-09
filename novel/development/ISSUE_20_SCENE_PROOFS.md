# Issue Twenty: four Goya scene proofs

## Selection and limits

Four plates now face their exact existing passages: The Next Drop (6-7),
Allow Two Days (12-13), A Room for the Cake (20-21), and The Heir to Seven
(22-23). The output is `output/pdf/ingenious-issue-20-goya-scene-proof-a3.pdf`.
It contains four A3 landscape reading spreads, not a complete issue or a
folding/imposition file. No printing was requested or performed in this pass.

Seven built-in image-generation calls produced four selected drawings: two
recovered pilots, two new scenes, and three targeted palette edits. Full prompts,
input/output hashes, selected native paths and individual reviews are in the
Issue Twenty illustration manifest. Temporary research photographs are not
republished. The Las Pozas plate uses the official garden's gothic-window image
for architectural forms; it is an interpreted fictional scene, not a surveyed
reconstruction. Goya's public-domain Capricho 43 supplies graphic language only.

Q retains the short long-sleeved jacket, segmented head, round ears, sampling
mouth and question-mark chest. The garden scene keeps his practical cap and
resting knee. Petra's bun, apron, broad features and practical humor remain
consistent between supper and key labeling. The driver is not Chano. The
wedding plate depicts Petra's remembered story: no present-day robot wedding.
The Custodian is absent, as required by this chapter.

The native images and all four complete rendered spreads were inspected.
Right-aligned crop on the supper image protects the driver's face; the other
plates use the established centered crop. All key hands, faces and captions
remain legible. The images use drawn contours and dark masses rather than
photographic surfaces. Q's fixed smiling mouth tends toward a modern cartoon,
however, and background hatching/tableware remain more descriptive than Goya's
most economical compositions. These are revision-proof selections, not A+ art
or final press masters. Eight Issue Twenty plates, including its cover, remain.

## Palette and typography

Palette edits remove the visible warm cast, but native RGB files retain maximum
channel differences of 20-24 levels; they are not mathematically grayscale.
The PDF converts them to DeviceGray with lossless image compression and no
downsampling. Shaded art remains shaded; no claim is made that every apparent
paper reserve in a drawing is exactly white. Text backgrounds are unpainted.
Cream should come from paper stock, not a printed text-page rectangle.

Georgia 14/19.8333, 197-point columns, existing continuous flow and left alignment
remain unchanged. The earlier justification pilot in `GOYA_ART_DIRECTION.md`
found a 22.33-point largest word gap versus 3.22 points left-aligned, despite
English hyphenation. That does not prohibit a better justified composition,
but it does rule out applying the tested version throughout the manuscript.

## Verification evidence

Baseline: `293ee18d`. `/tmp/check-ingenious-issue20-scenes.py` passes:

- Exact extracted words by spread: 267, 255, 281, 274 (1,077 total).
- Four A3 landscape pages, zero rotations, full-trim images and embedded fonts.
- Four lossless native-size grayscale image streams, 1024 by 1536 pixels,
  approximately 150 dpi at comic trim; not a 300-dpi press master.
- Seven reference hashes and selected source/asset hashes match. Complete
  prompts and all seven output hashes are retained for provenance.
- The English manuscript and outline, all 22 actual source/facing bindings and the
  other 21 manifests are unchanged. All 38 earlier issue PDFs are unchanged.
- The complete-issue production gate correctly rejects this partial art set.

PDF SHA-256:
`3c12d251dbbb00690bd8fc297e59ff17350d0470a455e8b9a86e23cfd846bbaf`.
Temporary build, verification and rendered inspection files are under
`/tmp/ingenious-issue20-scenes/`. Broader literary/cultural review, remaining
illustrations, earlier style correction and Spanish synchronization continue.
