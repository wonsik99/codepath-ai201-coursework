# PathReview Contribution Journal

## Week 7 - Issue Selection

**Issue:** [#75 - Add integration tests for the full safety middleware chain](https://github.com/ascherj/pathreview/issues/75)

**Tier:** Tier 2

The safety components only had isolated unit tests. The selected issue asked for
fixtures and integration coverage that sent requests through prompt defense,
content filtering, bias detection, and PII scrubbing in sequence. The scope
matched my Python testing experience and was small enough to complete during
the contribution module.

**Branch:** `feat/75-safety-integration-tests`

**Setup:** The application ran locally at `localhost:5173`, and the issue was
added to the cohort ledger.

## Week 8 - Reproduction and Planning

I added a deliberately failing integration-test skeleton to demonstrate the
missing coverage before implementing the solution.

- Reproduction commit: `8ea5e378f27b797acc48940db27fdf2aa2ef0e5f`
  (recorded in the [PR metadata](./pr-323.json)).
- [Archived original solution plan](./pr-323.patch), with a
  [curated reading copy](./PLAN.md).

There were no known blockers at this stage.

## Week 9 - Solution and PR Submission

I implemented `run_safety_pipeline()` inside
`tests/integration/test_safety_integration.py`. It chains the four safety
components in the documented order and makes the blocking layer visible through
the raised error.

The 14 tests cover:

- four clean-input and PII-redaction cases
- four prompt-injection cases
- one harmful-content filtering case
- two bias-detection cases
- three precedence and empty-input edge cases

All 14 contribution tests passed with `make test-integration`.

**Pull request:** [ascherj/pathreview#323](https://github.com/ascherj/pathreview/pull/323)

### Verification Clarification

The original Week 9 journal checked both `make check` and `make test-unit` as
passing, then stated that `make test-unit` had 53 failures. The accurate archival
record is:

- The 14 new integration tests passed.
- Checks scoped to the modified files were reported as passing in the PR.
- The complete upstream unit suite was not green: it contained 53 pre-existing
  failures in unrelated modules.
- The upstream type-check path also encountered a pre-existing NumPy stub syntax
  error.
- No additional failure was attributed to this contribution in the submission
  comparison.

## Week 10 - Iteration and Reflection

### Reviewer Feedback

Copilot reviewed all three changed files and identified the contradiction in the
Week 9 verification statement. The archival wording above incorporates that
feedback. At the August 12, 2026 consolidation, the GitHub review thread was
outdated and unresolved, and the upstream PR was still open. The latest recorded
submission status is kept in the [contribution overview](./README.md).

No human reviewer approval was recorded by the time this coursework archive was
consolidated.

The submitted code, complete final-state patch, and commit metadata were later
preserved locally on October 18, 2026 as closeout preparation. This archival step
does not mean that the upstream PR was merged or closed.

### What Was Harder Than Expected?

The four components expose different APIs. `PromptDefense.is_injection_attempt()`
is a static method returning a boolean, `ContentFilter.filter()` returns a tuple,
`BiasDetector.detect_bias()` also returns a tuple, and `PIIScrubber` must be
instantiated before calling `scrub()`. There was no single document covering
those signatures, so I traced the implementation and existing unit tests.

### What Did I Learn About Large Codebases?

Contributing to someone else's code requires more reading than writing. Before
adding tests, I navigated `safety/`, compared patterns in `tests/unit/`, and read
`CONTRIBUTING.md`. I also learned to separate failures introduced by a change
from failures that already exist in the target repository.

### How Did AI Tools Help, and Where Did They Fall Short?

AI helped generate test scaffolding and suggest edge cases such as whitespace
input and multi-violation payloads. It could not reliably infer the exact regex
and return-value behavior of the existing components; reading the source was
necessary to construct inputs that exercised each layer.

### What Would I Do Differently?

I would build the suite in smaller batches. Implementing two or three tests,
running them, and then expanding would expose API misunderstandings earlier than
planning all 14 cases first.

### What Am I Most Proud Of?

The layer-ordering test demonstrates why integration coverage matters. A payload
containing both injection and biased language is caught by `PromptDefense` first
and never reaches `BiasDetector`, proving a behavioral guarantee that isolated
unit tests cannot establish.
