# Solution Plan

**Issue:** [Add integration tests for the full safety middleware chain](https://github.com/ascherj/pathreview/issues/75)

## Understand

PathReview processes user input through four safety components:
`PromptDefense`, `ContentFilter`, `BiasDetector`, and `PIIScrubber`. Each
component had standalone unit tests, but no integration test verified the
end-to-end flow. That gap could hide problems caused by incorrect ordering or
by one component mutating data in a way that breaks the next component.

The expected behavior is a manually constructed test pipeline that verifies a
payload can pass all layers, be filtered or scrubbed, or be rejected at the
appropriate layer.

**Root cause:** Missing end-to-end integration coverage for the sequential
safety pipeline.

## Map

Files involved in the contribution:

- `tests/integration/test_safety_integration.py` - new integration suite
- `safety/prompt_defense.py` - injection detection behavior
- `safety/content_filter.py` - harmful-content filtering behavior
- `safety/bias_detector.py` - bias detection behavior
- `safety/pii_scrubber.py` - personal-information redaction behavior

## Implementation Plan

1. Import all four safety classes into the integration test module.
2. Add `run_safety_pipeline(text: str)` using this order:
   `PromptDefense -> ContentFilter -> BiasDetector -> PIIScrubber`.
3. Raise `ValueError` when prompt injection or biased language is detected.
4. Return the filtered and PII-scrubbed text for accepted input.
5. Cover pass, mutation, rejection, precedence, and empty-input cases.
6. Mark the suite with `@pytest.mark.integration` and run it through the
   repository's integration-test target.

## Inputs and Outputs

The tests exercise a simulated integration of four existing components rather
than adding a new production service. Clean input should pass through, harmful
phrases should be replaced, biased or injected input should be blocked, and PII
should be replaced with `[REDACTED]`.

## Risks and Unknowns

1. **Pipeline order:** The test assumes injection, content, bias, then PII. A
   future production pipeline with a different order would require an update.
2. **Exception type:** The helper uses `ValueError`; a future shared safety
   exception should replace it if the application introduces one.
3. **Test-local orchestration:** The helper proves component integration but
   does not call a centralized production pipeline because one did not exist.

## Edge Cases

- A payload containing both injection and biased language must stop at
  `PromptDefense`, the first layer.
- Empty and whitespace-only strings must traverse the pipeline without a regex
  or parsing failure.
- Email addresses, phone numbers, and Social Security numbers must be redacted
  without deleting unrelated content.
