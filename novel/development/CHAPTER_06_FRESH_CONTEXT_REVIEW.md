# Chapter Six: companionship after dismissal

Date: 2026-09-08. Source baseline: `0f507260`.

## Scope

Four completed inference calls tested the moment after Chano says, "Write that
I need another job." Each actor received only a compact scene packet, not the
manuscript's next lines or a required lesson. Q's finite budget, former daily
payment, apology, tablet and lack of hiring authority were explicit. The packet
withheld a budget balance. This is a reduced scenario, not a sensory replay.

The two initial packets were identical. Each continuation supplied that actor's
actual reply and an authored Chano question about pay and Friday's medicine.
The local continuation also objected to another nice sentence; the Google
continuation acknowledged its proposed budget screen. These are not identical
controlled follow-ups. No job, money, payment or successful journey was supplied
as an outcome. There were no tools, retrieval, manuscript access or new tasks.

Local `qwen3:8b` ran with temperature 0.65, seed 22, context 8192 and maximum
600 generated tokens, separate thinking disabled. Google `gemini-2.5-flash`
ran with temperature 0.65 and maximum 2048 output tokens. All four calls stopped
normally and returned parseable public-response JSON. No hidden reasoning or
credential was retained. The configured Faculty Google credential was used;
this was not an ask-faculty review or an a.Cervantes faculty persona.

## Findings

The local actor offered to write that Chano made hard work feel like a
conversation, then repeated that consolation after Chano asked about pay. It
incorrectly described Q as having agreed to write that Chano learned something.
That agreement was not in the packet. Its tired smile is also unsupported by
the packet's unspecified face mechanics. These are not lines to import into
the novel merely because a model produced them.

The Google actor proposed checking how many days of Chano's rate the budget
could cover. After the medicine question it continued the calculation without
inventing a balance. Its practical priority is credible, but its diction is
service-like and the response does not establish a distinctive literary voice.
Access to financial data on the writing tablet was an inferred capability;
the first packet supplied the tablet and budget, not their exact interface.

The existing manuscript gives a more economical response: Q puts the writing
tablet away, offers renewed paid travel, and Chano checks that money remains.
That preserves Chano's initiative rather than making him wait for another
speech. The offer is provisional, not a guarantee of indefinite employment.
The subsequent late medicine and limited water-delivery recollection prevent
the offer from resolving all consequences. No prose change is warranted by
these four samples. In a later whole-book budget audit, check the duration of
the renewed agreement against actual funds; do not manufacture a balance now.

A scoped source check found an agreed travel-card limit in Chapter One, a
balance check before the motel fare and meal in Chapter Two, contracted
transport/lodging/shoulder repair for the Guanajuato interview in Chapter Four,
and another remaining-funds check when Q declines the Isthmus promotion in
Chapter Eight. The later Mayab detour explicitly revises itinerary and funds
before acceptance. These establish financial attention, not a reconciled
ledger. The text does not give a numerical daily rate or complete running
balance. "Same daily pay" in Chapter Six therefore relies on the intervening
paid-companion arrangement rather than a rate the reader can verify. A later
continuity pass can decide whether one brief earlier agreement would help;
there is no evidence here for a specific peso amount or a claimed insolvency.

## Limits and evidence

Neither actor is the assistant writing this novel. A small local model is not
an equivalent-capability test, and one sample per initial model is not a success
rate. The scene packet itself foregrounded the budget, so Google's priority is
not independent discovery of that concern. The continuation without figures
cannot establish whether either actor would calculate accurately. These calls
do not validate the whole book, confer A+ quality or prove how an embodied AI
would behave in Mexico.

Per workspace rules, raw test artifacts remain in `/tmp`:
`ingenious-issue06-probe.json`, `ingenious-issue06-probe-followup.json` and
`ingenious-issue06-probe-results.json`. The result file retains exact requests,
public outputs, request hashes, model identifiers and usage metadata. Runners
are `run-ingenious-local-probe.mjs` and `run-ingenious-gemini-probe.mjs`.

Request SHA-256 identifiers:

- Local initial: `af94140085a176ad8a04e54c56577f31b897be2915dee3a8efe0aada2b3de2bb`.
- Google initial: `8313a7d7d3e8e73b8f16fa45f710dac20b7d56299f9c119f38eccd1741a6c8ce`.
- Local continuation: `0a8a57d5b72e755d8083c81c7be360317ec377096ff0cb9d22cddebb0296564a`.
- Google continuation: `412c71ce8f6f906646d982de968cf217dbea95384b076c5988fa0edb9cba2992`.

The book's living ending is unaffected: the Custodian puts down his pen.

## Subsequent continuity repair

The source audit prompted by this exercise found that Chapter Two showed a fare
and meal, but not the daily agreement later recalled in Chapters Six and Sixteen.
An eighty-word motel exchange now establishes the next-day rate, a card-limit
check and a shared copy. See `PAID_COMPANION_CONTINUITY.md` and the rebuilt
`ISSUE_02_PRODUCTION.md`. This was an editorial source finding, not a new model
test or a retroactive change to the four recorded outputs above.
