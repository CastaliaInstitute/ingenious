# Motivation revision: working record

## Active objective

Revise both books around Q's choice to explore Mexico and keep writing with the
Custodian. Test his behavior in representative scenes; preserve eloquence, humor,
Mexican specificity, and other characters' agency. Reconcile the outline and
illustrated issues, verify affected print PDFs, and push the revision.

The latest user clarification governs the ending: “Death just means we finish
the book.” The source now permits Q to remain alive when the writing stops.

## Evidence so far

- `Q_DESIGN.md` contains the current motivation and simulation design. The prior
  hidden planning block was preserved in `2026-09-07-superseded-planning.md` and
  removed from the manuscript. Its compulsory sacrifice is no longer authoritative.
- Chapter 1 establishes memory summaries that can distort, local commitments,
  budget, charge, physical limits, an adopted journey, and an evening call.
  Its interludes replace elementary semantic failures with missing context and
  administrative ambiguity. Amealco is rendered as wooded highland terrain.
- Chapter 2 now begins with Q seeking a socket. He saves Chano's dismissal notice,
  makes an unjustified access assumption, and presses a stop too early. The
  resulting damage and security incident lead to the viral clip. The governorship
  begins as a joke in a paid companionship agreement. Q calls home and amends his
  plan. The motel, water vendor, and scrubber interludes have continuity repairs.
- Chapter 3 preserves Lucía's work and central objection. Q apologizes, asks a
  practical question, and accepts a follow-up task for the petition. He can still
  confuse a good autobiographical sentence with the requested incident report.
- Chapter 4 and both interludes now distinguish Q's negotiated appearance license
  from Castalia's disputed body ownership. The Custodian offers an alternative;
  Q admits wanting travel, repair, and an audience. Estela remains the interviewer.
  The employment-profile exposure comes from an unchecked automatic attachment,
  not Q investigating a critic's home. Don Hilario's copying and quotation limits
  are respected; later trial references still need reconciliation.
- Chapter 5 and its three interludes replace elementary misunderstanding with
  specific errors in promised software independence, geographic anonymity, and
  recording permission. The route enters eastern Michoacán's oyamel forests.
  Local speakers disagree rather than supplying a uniform indigenous position.
  Q can comfort a child, help fix a logging setting, and respect a refusal.
- Chapter 6 distinguishes the mayor's authority from the marketed governorship.
  Q maintains calls, repair needs, paid companionship, and the agreed forest
  inspection. The hose fitting is delivered successfully. His writing project
  also gives him a reason to overlook the burdens Chano faces at the office.
- Chapter 7's main narrative now uses a specific records appointment to bring
  Lucía into the itinerary. Q remembers signing the petition and follows up the
  address confirmation. Ofelia's scene lets him be helpful without forcing a
  privacy failure. The Menard seminar tests an unchanged opening against changed
  experience, then exposes a link between public and unpublished information.
  The museum transition is repaired; its four interludes remain to be revised.
- Chapter 22 and the coda have been rewritten. Q verifies the power problem,
  obtains help from Q-Prime, saves permissions, survives, and finishes the book
  with the Custodian. Ownership and maintenance disputes remain open.
- `Q_SCENE_EXERCISES.md` records four author-run exercises with limited packets,
  alternative responses, consequences, and editorial findings. These are not
  independent blind runs; the limitation is explicit.

## Required next work

1. Read and revise Chapter 7's four interludes and Chapters 8-21. Trace promises,
   calls, battery and funds, Castalia's control, the restricted index, and the
   difference between Q's public identity and his current commitments. Avoid
   making every person a dispenser of a moral lesson.
2. Repair backward references to the changed first encounter, Dulcinea claim,
   payment, surveillance, and the ending. Check the trial's quoted evidence.
3. Continue reconciling `OUTLINE.md` as the middle chapters are revised. It now
   reflects Chapters 1-6, Chapter 7's main narrative, and the ending. Its remaining
   summaries explicitly describe material that still needs a revision pass.
4. Extend the scene exercises. Use fresh context if a suitable runtime can be
   invoked; do not report author-known outcomes as independent validation.
5. Rebuild the English chapter issues only after text and plate placement are
   reconciled. The existing PDFs predate this revision. They are not evidence of
   the new story. English is the current revision source; the Spanish edition
   remains an earlier translation and must be labeled accordingly if linked.
6. Inspect plates against the actual facing text after pagination. The existing
   builder uses modulo indexing and will silently repeat plates if the number of
   text pages changes; remove that behavior. Its current odd-page art followed
   by even-page text also requires a facing-spread audit in a bound booklet.
7. Restore the requested print specifications: readable larger text, continuous
   flow, black ink and unpainted text backgrounds for cream stock, captions in a
   margin, full-bleed art, and the 24-page/12-plate/six-sheet Issue 1 proof. Verify
   A3 landscape imposition and short-edge duplex orientation. Do not print before
   the requested quality review.
8. Render and inspect PDFs, check full text coverage and no repetition, validate
   links and page sizes, and commit/push completed changes. The goal remains active.

## Located build tools

The repository's existing development scripts live in `/tmp`, as required by its
AGENTS.md:

- `/tmp/build_chapter_issue_set.py`: all 22 English issues, hard-coded image maps,
  477 x 738 points, 8.8-point body text, currently colored ink.
- `/tmp/build_ingenious_serial.py`: complete serial builder and shared styles.
- `/tmp/build_issue1_en.py`: separate Issue 1 proof, depends on the serial builder.
- `/tmp/impose_issue1_a3.py`: 24-page imposition, 12 A3 sides, paired outer/inner
  pages, no reverse-side rotation; needs rendered verification with current files.
- `/tmp/build_ingenious_pdfs.py` and `/tmp/generate_ingenious_pdfs.py`: additional
  complete-book builders, not yet inspected for this pass.

The PDF skill has been read. Before first PDF authoring, locate and run its
artifact-operation marker once if available. Intermediate renders and diagnostic
scripts belong under `/tmp`. No PDF has been rebuilt in this pass.
