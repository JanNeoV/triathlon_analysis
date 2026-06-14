# Chasing Ghosts in Ironman Data: V2 Writer Guide

## Core Thesis

The article should now make one stronger distinction:

> Some anomalies are athletes, some are rows, and some are whole races.

That is the answer to the 100% hard-rate problem. If nearly everyone in a race has an impossible swim speed, the best interpretation is not "nearly everyone is suspicious." It is "the swim probably was not the nominal distance, or the timing/source data represents the event differently."

## What Changed In V2

The notebook now separates three review families.

Event/course context:
This catches likely shortened, cancelled, altered, unusually long, or differently recorded legs. A high hard-rate belongs here when it clusters across the whole event.

Strict record integrity:
This catches rows that do not add up in a hard way: overall time mismatch, a split equal to the overall time, or an extreme transition value.

Rank audit:
This catches source rank fields that disagree with ranks recomputed from the times. It is a caveat, not a standalone verdict. Rank mismatch alone should not turn a case into high-confidence record integrity.

Individual profile:
This catches unusual profiles only after event context and record integrity issues are removed.

## How To Explain Hard Limits

Do not say "hard limits detect impossible athletes."

Say:

> Hard limits first test what would be impossible if the event used the standard distance. Then the notebook asks whether that impossibility belongs to one athlete or to the whole race.

This is the most important nuance in the article.

## How To Explain The Five Cases

Case A:
This should be explained as a profile surprise, not a broken row if the only row-level issue is rank audit. The athlete is very strong in swimming, very weak on the bike, and roughly okay on the run. That spread plus the model residual makes it review-worthy, but the rank mismatch is only a caveat.

Case B:
This is a record-integrity issue. The row has a duplicate or unusual split relationship and an extreme transition/reconciliation problem. This is the cleanest example of "the row itself does not make sense."

Case C:
This is the key V2 example. It should no longer be explained as a simple hard-limit athlete anomaly. It is better framed as event/course context: the row looks impossible only if we assume the standard swim distance.

Case D:
This is a consistency-only profile. It may be real specialisation or fatigue, so it is interesting but lower severity.

Case E:
This is a model-residual profile. It is the highest-uncertainty family because the model sees a surprising relationship, but the data cannot tell us why.

## Article Structure

1. Open with the 100% hard-rate puzzle.
   Explain that the first notebook found some races where nearly everyone was "impossible." That is not a scandal; it is a clue that the method needs course context.

2. Define the three review families.
   Event context, record integrity, individual profile.

3. Show before/after hard flags.
   This is the article's strongest methodological improvement.

4. Show course-context candidates.
   Present these as "likely altered event legs," not as athlete anomalies.

5. Show record-integrity examples.
   Use Case B style examples to explain duplicate times and reconciliation mismatch.

6. Show individual profile surprises.
   Use consistency and residual cases only after context adjustment.

7. Add the PRO/non-PRO sensitivity check.
   Use this to answer the fair reader question: are elite athletes being flagged just because they are elite?

8. End with the broader lesson.
   Data science is not only about finding strange rows. It is about asking what kind of strange they are.

## How To Read The Figures

Hard-flag decomposition:
Read this from broad to narrow. Nominal hard rows are what looks impossible under standard-distance assumptions. Event-context rows are likely explained by shortened, cancelled, or atypical event legs. Remaining individual hard rows are the small set that still looks extreme after that adjustment.

Course-context heatmap/table:
Use this as the simpler main article visual. It reads like a matrix: leg on one axis, hard-rate band on the other, with each cell counting event-legs and affected rows. It translates event hard-rate into reader language: normal tail, ambiguous review zone, likely event context, probable event context.

Non-normal course-context bar:
This companion chart removes the normal tail so the reader can see where altered-leg candidates concentrate without being drowned by standard events.

Review-family small multiples:
Read each panel separately. Event context, strict record integrity, and individual profile are different kinds of review signal and should not be forced into one blended bar.

Sensitivity panels:
Each threshold family answers a different question. Do not compare the line heights across panels as if they were the same metric.

Review examples matrix:
Read this as evidence, not a verdict. The rows are anonymised examples; the swim, bike, and run cells show percentile within the same event-gender field; the side label lists the review family and numeric clues.

Huber residual dumbbell:
Each row runs from predicted percentile to actual percentile for the target leg. A large gap means the leg relationship is surprising after accounting for the other two legs and division.

PRO/non-PRO sensitivity:
Read this as a robustness check. PRO rows are useful for testing whether the method mistakes elite performance for anomaly. They are not a good source for individual public examples because the cohorts are small.

## What High Rates Mean

A high nominal hard-rate usually means the event leg is different from the nominal assumption. It should push the article toward course context, not toward individual suspicion.

A mid-range nominal hard-rate is ambiguous. This is where the method asks for review, not where it claims certainty.

A low nominal hard-rate can be a better place to look for individual rows, but only after record integrity and event context are checked.

## Figure Captions

Before/after hard flags:
"Many nominal hard flags disappear once race-level course context is separated from individual profile review."

Course-context candidates:
"A clustered hard-rate usually points to an altered event leg, not to hundreds of suspicious athletes."

Review family rates:
"The revised workflow separates race-context, row-integrity, and athlete-profile signals."

Consistency spread after context adjustment:
"Removing likely altered event legs makes the remaining profile surprises more meaningful."

Sensitivity chart:
"The exact review rate changes with thresholds, but the separation between event context and individual review is the important result."

Course-context heatmap/table:
"When high nominal hard-rate rows cluster inside the same event-leg, the signal points toward course context rather than individual athlete behaviour."

Non-normal course-context bar:
"Removing the normal tail makes the altered-leg candidates easier to see."

Review examples matrix:
"Each row shows the evidence behind a review flag without naming the athlete or turning the row into a verdict."

Huber residual dumbbell:
"Huber residual examples compare what the model expected for one leg with what the result row recorded; the flag is a surprising relationship between legs, not a label on athlete ability."

PRO/non-PRO sensitivity:
"Splitting PRO from non-PRO rows checks whether the review layers are reacting to elite consistency or to actual leg-to-leg surprises."

## Language To Use

Use:

- nominal-distance flag
- event-context candidate
- strict record-integrity issue
- individual profile surprise
- course-context adjustment
- review family
- likely altered event leg
- surprising relationship between legs
- model residual review

Avoid:

- cheating detector
- guilty
- busted
- suspicious race
- impossible athlete list
- hard flags prove anomalies
- slow athlete anomaly
- fast athlete anomaly

## How To Phrase Model Flags

Do not say "the model finds slow or fast athletes."

Say:

> The model flags rows where one leg is much stronger or weaker than the other two legs and the athlete's division would lead us to expect.

This is why elite athletes are not automatically model anomalies. An athlete who is excellent across swim, bike, and run is internally consistent. The model becomes interested when the relationship between legs breaks that pattern.

The notebook includes `model_flag_examples` and a Huber residual dumbbell so the article can show this visually without exposing athlete identities.

## How To Use The PRO Check

Use non-PRO rows as the main population for individual-profile discussion.

Use PRO rows as a sanity check:

- consistent elite athletes should not be flagged merely because they are fast
- model flags should appear when one leg breaks the expected swim-bike-run relationship
- event-context flags should mean the same thing for PRO and non-PRO rows

Use the main model-rate comparison as the article-facing check. Treat separate PRO-only Huber models as a calibration stress test: if their sample flag rates are higher, that may simply mean the PRO residual scale is much tighter.

Avoid publishing individual PRO examples by default. PRO cohorts are small, so even anonymised examples can become easier to identify.

## How To Use Case Evidence

The notebook now keeps case outputs as data-only evidence. It does not generate final verdict prose for the article.

Use the evidence table and review examples matrix to write your own explanation:

- what triggered the review family
- what the numbers show
- what plausible non-accusatory explanations remain
- what the data cannot prove

## Limitations

The notebook infers course context from result patterns. It does not know the official course decision unless you manually verify it.

Known examples show that swims and even whole events can be shortened or cancelled because of current, water quality, storms, heat, or safety concerns. The notebook uses those examples as validation, not as required metadata for every race.

The model residual layer is useful but uncertain. It should support the story, not carry it.

## Technical Methodology

For the GitHub-facing explanation of thresholds, cleaning, event-context logic, hard-flag adjustment, and Huber residual models, see [chasing_ghosts_methodology.md](chasing_ghosts_methodology.md).

## Sources To Mention If Useful

- Ironman Louisville 2018 swim was shortened from 2.4 to 0.9 miles due to strong currents: https://de.wikipedia.org/wiki/Ironman_Louisville
- Ironman South Africa had multiple swim reductions/cancellations in recent editions: https://de.wikipedia.org/wiki/Ironman_South_Africa
- Ironman New Zealand 2012 was shortened to 70.3 distance: https://en.wikipedia.org/wiki/2012_Ironman_World_Championship
- Ironman 70.3 examples include shortened or cancelled swims and shortened bikes/races: https://en.wikipedia.org/wiki/2012_Ironman_70.3_World_Championship
- Huber regression is useful because it reduces outlier influence without fully ignoring outliers: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html
