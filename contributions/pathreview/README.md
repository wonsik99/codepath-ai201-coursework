# PathReview Contribution (Weeks 7-10)

This directory documents my contribution to
[PathReview](https://github.com/ascherj/pathreview), an existing AI-powered
portfolio review application. I did not create the full PathReview codebase.

## Contribution

| Item | Link or value |
|---|---|
| Upstream repository | [ascherj/pathreview](https://github.com/ascherj/pathreview) |
| My fork | [wonsik99/pathreview](https://github.com/wonsik99/pathreview) |
| Selected issue | [#75 - Add integration tests for the full safety middleware chain](https://github.com/ascherj/pathreview/issues/75) |
| Pull request | [#323 - test: implement full safety middleware integration tests](https://github.com/ascherj/pathreview/pull/323) |
| Branch | `feat/75-safety-integration-tests` |
| Pull-request head | `65b015a5dc1697c811e0a4f323a4bfb89a32fdac` |

The change adds a test-local pipeline that exercises these components in order:

```text
PromptDefense -> ContentFilter -> BiasDetector -> PIIScrubber
```

Fourteen integration tests cover clean input, email/phone/SSN redaction,
prompt-injection blocking, harmful-content filtering, bias blocking,
multi-violation precedence, empty input, and whitespace-only input.

## Weekly Timeline

- **Week 7:** Selected and scoped the Tier 2 safety integration issue.
- **Week 8:** Reproduced the missing coverage and wrote the solution plan.
- **Week 9:** Implemented 14 tests and opened the upstream pull request.
- **Week 10:** Completed the course reflection and reviewed the submission state.

## Verification Record

- `make test-integration`: 14/14 contribution tests passed.
- The upstream project had 53 pre-existing unit-test failures in unrelated
  modules; the contribution introduced no additional failures according to the
  submission comparison.
- A pre-existing NumPy stub parsing error also prevented the complete type-check
  suite from being fully green.

The original journal simultaneously marked the full unit suite as passing and
then documented its 53 existing failures. This archive corrects that
contradiction instead of repeating it.

## External Status

As checked on August 12, 2026:

- The coursework contribution and reflection are complete.
- The upstream PR is open and mergeable but has not been merged.
- Issue #75 remains open.
- A Copilot review noted the verification wording contradiction. The thread is
  outdated but still unresolved on GitHub.
- The latest GitHub Actions run ended with `action_required` and created no
  jobs, so it does not represent a completed CI test run.

PathReview remains in its separate fork so PR #323 and its source commits stay
connected to the upstream review.

## Archived Documents

- [Solution plan](./PLAN.md)
- [Weekly journal and reflection](./JOURNAL.md)
