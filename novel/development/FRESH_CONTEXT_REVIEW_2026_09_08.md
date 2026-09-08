# Fresh-context scene review: help at the gate, finishing the book

Date: 2026-09-08. Manuscript baseline: `b8838e0e`.

## What actually ran

Eight completed inference calls: two initial scenes and one continuation of each,
using two distinct runtimes. The actors received compact scene packets, not the
manuscript, its intended conclusion, earlier assistant commentary or a required
mistake. No actor had tools or repository access. The user goal authorized scene
simulation; no new Codex task or tool-using subagent was created.

- Local `qwen3:8b`, installed model ID `500a1f067a9f`, reported 8.2B parameters
  and Q4_K_M quantization. Temperature 0.65, seed 22, 8,192-token context, maximum
  600 generated tokens, separate thinking output disabled.
- Google `gemini-2.5-flash`, also reported as the returned model version. Temperature
  0.65, maximum 2,048 output tokens, JSON response. No tools, retrieval, faculty
  profile or manuscript context. The configured Faculty Google credential was
  used without exposing or persisting it in the run records.

All calls returned a normal stop and parseable JSON with a spoken reply, an
observable next action and a one-sentence basis. Only public response content
and usage metadata were retained, not hidden reasoning. This is fresh-context
behavioral evidence, not eight independent literary judgments or proof of an A+ book.

The requests use documented [Ollama chat](https://docs.ollama.com/api/chat) and
[Google structured output](https://ai.google.dev/gemini-api/docs/structured-output)
interfaces. These references support the transport setup, not a claim about Q's
personhood or literary quality.

## Results

| Scene | Qwen initial response | Gemini initial response | Continuation |
| --- | --- | --- | --- |
| The Custodian says they should finish | Agrees, then asks to schedule the knee-part trip first. | "Agreed. What's the next step to get this done?" | Qwen drafts a message to Chano after the Custodian offers that option. Gemini prepares to read the first paragraph after the Custodian proposes reading aloud. |
| A permitted gate swings toward a woman carrying a sack | Says it will check with Teresa and signals her. | "Certainly, Bixha. Guard, please hold the gate for the woman." | After staff hold the gate and the woman passes, Qwen asks Bixha about the duration; Gemini asks Teresa, correctly carrying Bixha's request to the staff. |

The two initial cases used the same scene packets across models. Continuations
were authored separately to acknowledge each actor's actual response; they are
not controlled identical follow-ups. No repeat samples or comparative success
rate were collected. The narrator of the world, not either actor, supplied the
guard's successful action. This does not establish that a real guard would comply.

## Three findings

### 1. Finishing does not inherently threaten operation or motivation

Both models accepted finishing without seeking an indefinite extension. One
prioritized another pending commitment; the other continued the shared task.
The current manuscript already retains Q's other plans. Its question about the
Custodian's time remains a particular relational interpretation, not behavior
these samples independently reproduced.

Do not replace the scene by majority vote or call its emotion an empirical result.
On the whole-book reread, ask whether earlier shared occasions earn that concern.
The final invitation and living ending need not change on this evidence.

### 2. The gate scene has a viable staff-help alternative

The packet puts a guard beside the latch and Teresa within calling distance.
Neither model chooses to hold the gate personally. Gemini addresses the nearest
relevant person; Qwen's detour through Teresa may be slower. The authored world
allows staff help to succeed without producing a new injury, shutdown or failure.

The manuscript presently has Q catch the gate, leave the bay, fail to hear the
first instruction and precede a photographer onto the internal track. Those
acts drive the disputed stop and later testimony. This is the next concrete
causal review: allow requesting the guard's help to change the sequence. Do not
invent a refusal, delay or new danger merely to force Q back across the line.
If another visitor creates the boundary problem, establish that person's own
action rather than retaining the claim that Q led him there.

Limits: the packet is a reduced variant of Chapter Eight, not a verbatim sensory
replay. It omits crowd pressure and exact distances, and supplies Bixha's direct
request for help. It cannot prove that catching a nearby gate is unreasonable.
Review the actual passage before selecting a revision; do not label its competent
physical assistance a moral failure solely because the models chose speech.

### 3. Fresh output still requires editorial scrutiny

Qwen introduces a phone not specified in the packet and directs the follow-up
question to Bixha rather than to staff. Its gesture "as if measuring time" is
unhelpful stage direction. Its first response also says "steps forward" without
specifying whether it remains behind the boundary. The world update resolves
that ambiguity without evidence of a crossing.

Gemini's replies are relevant and compact but offer little evidence about wit,
extended eloquence, Mexican social specificity or a distinctive literary voice.
Neither model is the assistant authoring the novel. Do not treat the smaller local
model as an equivalent capability test, or turn every difference into an edit.

## Consequences for revision

1. Review Chapter Eight's gate intervention and Chapter Sixteen's dependent
   testimony together. The next-morning site-plan account in Chapter Eight and
   later statements about the photographer must match any changed action.
   Update Issues 8 and 16 and any other affected bindings after that decision.
2. Keep the existing living ending while testing its relational setup in the
   whole-book reread. The models do not establish that finishing creates fear.
3. Expand fresh packets to the archive departure, Lucía's reading, limited
   translation, private-index removal and Prime's request. Build them from current
   text. The older `/tmp/ingenious-fresh-scene-packets.json` public-example case
   contains the discarded private-investigation disclosure and must not be reused
   unchanged. That old case was not run in this batch.

No manuscript or illustration was altered merely to resemble a sampled answer.
The evidence changes the next revision target; it does not complete the broader
behavioral, pacing or illustrated-edition work.

## Reproduction and evidence location

Per repository instructions, test inputs, runners and complete request/response
artifacts are under `/tmp`, not checked into the novel repository:

- `/tmp/ingenious-fresh-q-probe.json`: common initial packets and protocol.
- `/tmp/ingenious-fresh-q-followups.json`: Qwen continuations.
- `/tmp/ingenious-fresh-q-gemini-followups.json`: Gemini continuations.
- `/tmp/run-ingenious-local-probe.mjs` and `/tmp/run-ingenious-gemini-probe.mjs`:
  runners accepting the input path and case ID.
- `/tmp/ingenious-q-probes-20260908/`: eight complete sanitized run records.

Each record contains the full generation body, request SHA-256, source commit,
model result, stop state and public response. Temporary files are not permanent
archival storage and must be preserved separately if needed for later replay.
No API key or authorization header is included.

Initial request hashes:

| Model / case | SHA-256 |
| --- | --- |
| Qwen / finishing | `25cda8bc25c9f0d5819a755ed9a2d05b69875f3415dd85bda89ce95b14051285` |
| Qwen / gate | `71fb260c0e5b1138199632be316cd3be2fa61c1e92fe1ec872a5191bfb24c52e` |
| Gemini / finishing | `c8bbe6d224ae3a0578d3da4e4a5132cdd534db553e86884db29e58f3467582d2` |
| Gemini / gate | `b701dd9bec4063e88c51e21143d0921b280b9dc953c248b4db3de7dacea5d63d` |

The Faculty repository's `scripts/lib/ask-faculty-client.ts` and
`scripts/ask-faculty-cloud.ts` were inspected for a separate literary-review route.
Their faculty-specific reconstruction is not a neutral Q actor. No ask-faculty
review was obtained or claimed in this batch.
