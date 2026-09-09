# Goya direction: governing correction

The user's 2026-09-08 correction overrides earlier stylistic approvals. The plates
must be in the style of Goya, not photographs with etched texture. An image can
match the facing scene and the cast while still failing the art direction.

## Visual language

Use Goya's *Los Caprichos* as the principal print reference: economical etched
contours, broad aquatint darks, paper-white reserves, compressed space and expressive
human gesture. Let faces be interpreted and slightly distorted. Detail should
serve the action, not cover every surface. Do not replace photographic realism
with generic vector cartoons or uniformly meticulous nineteenth-century engraving.

The comedy should come from the encounter, pose, scale and juxtaposition. Do not
add donkeys, owls, devils, grotesque crowds or supernatural events merely because
they occur in Goya's source prints. Nor does this direction authorize caricaturing
Mexican ethnicity or treating residents' complaints as stupidity.

Contemporary Mexican clothes and infrastructure remain contemporary. No compulsory
knightly costume. Q stays recognizable through a narrow segmented oval head,
circular ears, slim articulated silhouette, short jacket and question-mark chest.
The right-knee support remains where visible. Exact rivet counts, photographic
faces, skin pores, fabric weave and lens-like depth are not continuity requirements.
The Custodian remains male, tall, long-haired and bespectacled.

Ink is neutral black/gray on white; cream comes from stock. The antique paper tone,
plate border and handwritten captions in museum scans are not to be copied into
new assets. Illustrations still reach comic trim and use separately typeset captions.

## Reference evidence

- Goya, *Tu que no puedes*, Capricho 42, 1799. The Metropolitan Museum of Art,
  object 370575, accession 18.64(42), etching and burnished aquatint.
  https://www.metmuseum.org/art/collection/search/370575
- Goya, *El sueño de la razon produce monstruos*, Capricho 43, 1799. The Met,
  object 338473, accession 18.64(43), etching and aquatint.
  https://www.metmuseum.org/art/collection/search/338473

Both collection API records mark their images public domain. Use them for graphic
language, not as literal scenes to duplicate. Native reference files and source
attribution accompany the new pilot manifest.

## Status and approval gate

Issue Fourteen's ten photorealistic PNGs and two PDFs are preserved as superseded
studies. Their manuscript revision remains valid. Do not call those images final
or use their previous approval flag to pass a build. Earlier Issues 1-13 retain
their historical technical checks but require a fresh style audit before they can
be accepted under this direction. A successful PDF check is not an artistic grade.

Start with two different narrative demands: Chano alone in the sinking office
chair, and Q joining his friends for lunch. Compare the selected drawings with the
actual prints at thumbnail and reading size. Check drawn contour, tonal hierarchy,
expressive gesture, reduced incidental detail, scene fidelity and Q identity.
Only then expand the replacement issue set; do not mass-produce a failed style.

## Typography pilot

Compare the same text and illustration with left alignment and with justified
body paragraphs using English hyphenation. Preserve headings and captions flush
left, paragraph final lines unstretched, current type size and the continuous
two-column reading order. Inspect spacing rather than assuming justification wins.
No global pagination or facing-text mappings change until a layout is selected.

### Pilot decision, 2026-09-08

The completed comparison favors left alignment at the current narrow measure.
Keep the production builder unchanged. At Georgia 13.3 points in a 197-point
column, the same 270 words and same image produced a largest interword gap of
3.22 points left-aligned versus 22.33 points justified, despite English
hyphenation. Both complete rendered spreads were inspected. This rejects the
tested composition, not all possible justified typography.

The two scene studies and a further lunch redraw are saved in
`output/illustrations/goya-pilot/`, with complete prompts and museum provenance
in its `manifest.json`. The chair study has the stronger tonal hierarchy. The
lunch redraw softens the modern-comic finish but does not yet solve Q's blank
oval mask or the posed grouping. None is an approved production master.

The solitary evening chair scene belongs to the cover concept or the passage on
text page 18. It must not replace the contractor inspection opposite text page
16 merely because both scenes involve the same chair. The lunch scene belongs
opposite text page 14. Existing issue mappings remain unchanged.

### Verification scope

The pilot's three PNGs and two museum references match their recorded hashes;
native PNG dimensions are 1024 by 1536. The Chapter Fourteen hash and both scene
anchors match the manuscript. All ten superseded issue assets and both superseded
PDFs match their preserved records, but the production approval gate rejects
that manifest. The other twenty-one chapters, living final sentence, all twenty-two
existing facing-text bindings and twenty-six earlier issue PDFs remain unchanged
relative to `9d8fe618`. These checks establish preservation and mapping integrity,
not an artistic grade or whole-book literary approval.
