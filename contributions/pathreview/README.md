# PathReview Contribution (Weeks 7-10)

This directory preserves my submitted contribution to
[PathReview](https://github.com/ascherj/pathreview), an existing AI-powered
portfolio review application. I did not create the full PathReview codebase.

## Contribution

| Item | Link or value |
|---|---|
| Upstream repository | [ascherj/pathreview](https://github.com/ascherj/pathreview) |
| Original fork (historical source) | [wonsik99/pathreview](https://github.com/wonsik99/pathreview) |
| Selected issue | [#75 - Add integration tests for the full safety middleware chain](https://github.com/ascherj/pathreview/issues/75) |
| Pull request | [#323 - test: implement full safety middleware integration tests](https://github.com/ascherj/pathreview/pull/323) |
| Branch | `feat/75-safety-integration-tests` |
| Pull-request head | `65b015a5dc1697c811e0a4f323a4bfb89a32fdac` |
| Merge base | `d5f196df22aebcfd3d1e3ded657b34ef77e3533e` |
| Snapshot date | October 18, 2026 |

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

## Historical Verification Record

The following results were recorded during the original submission. They were
not rerun while preparing this archive.

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

As checked on October 18, 2026:

- The coursework contribution and reflection are complete.
- The upstream PR is open, mergeable, and awaiting review (`REVIEW_REQUIRED`).
  It has not been merged or closed.
- The separate fork still exists and has not been deleted.
- The [recorded GitHub Actions run](https://github.com/ascherj/pathreview/actions/runs/30963654423)
  ended with `failure` on September 4, 2026, with zero jobs. It does not establish
  whether the tests passed or failed.

Only closeout preparation has been completed. The archive must be published and
verified before any fork deletion. See the [closeout checklist and unsent
comment draft](./CLOSEOUT.md).

## Archived Files

- [Exact submitted test source](./snapshot/tests/integration/test_safety_integration.py)
- [Complete final-state PR patch](./pr-323.patch)
- [PR metadata, commit IDs, and expected file hashes](./pr-323.json)
- [SHA-256 checksums](./SHA256SUMS)
- [Solution plan](./PLAN.md)
- [Weekly journal and reflection](./JOURNAL.md)

The patch preserves all three submitted files unchanged: `JOURNAL.md`,
`PLAN.md`, and `tests/integration/test_safety_integration.py`. It therefore also
preserves the original journal's inconsistent verification wording. The curated
documents linked above explain the correction; the original patch is not edited
to rewrite the submission record.

This snapshot is not a full fork or Git-history backup. The original fork URL is
retained only for provenance and may become unavailable after cleanup. The
submitted code and final patch are stored here rather than relying on that URL.

## Archive Integrity

On October 18, 2026, the patch was applied in a fresh temporary Git repository.
All three resulting Git blob hashes matched the PR head, and the restored test
file was byte-for-byte identical to the standalone snapshot. Python syntax
validation found 14 test definitions. These checks verify the archive, not the
runtime behavior of the upstream application.

To check the archived files from this directory:

```bash
shasum -a 256 -c SHA256SUMS
```

The patch uses PathReview's original file paths. To restore it, use a separate
PathReview checkout at the merge-base commit listed above, then run
`git apply --check /absolute/path/to/pr-323.patch` before applying the patch.
Do not apply it at this coursework repository's root. Running the tests requires
PathReview's safety modules and dependencies, which are not included here.
