# Spec 002: File Selection and Move Safety Unification

## Objective
Ensure file inclusion and exclusion behavior is consistent between non-recursive and recursive modes, with predictable and safe move behavior.

## Background
Current traversal paths can apply different filtering logic, which can move files unexpectedly in recursive mode.

## In Scope
1. Unify selection logic used in all traversal modes.
2. Apply identical exclusion policy across top-level and recursive traversal.
3. Define behavior for dotfiles and multi-extension files.
4. Define deterministic conflict behavior when destination file already exists.
5. Add robust tests using filesystem fixtures.

## Out of Scope
1. New CLI UX features unrelated to safety.
2. Packaging/version concerns.
3. Large refactors unrelated to selection/move semantics.

## Policy Decisions (Locked)
1. Dotfiles are excluded by default.
2. Exclusion checks must be identical in recursive and non-recursive workflows.
3. Collision behavior must be safe and deterministic.
4. Any skipped file should be explainable by one clear policy rule.

## Functional Requirements
1. One shared predicate determines whether a file is eligible for movement.
2. Exclusion list behavior supports:
   1. exact-name exclusions
   2. suffix/pattern exclusions where intended
   3. hidden-file default exclusion
3. Recursion depth boundaries must be strictly enforced.
4. Existing destination conflicts must follow one policy:
   1. skip and report, or
   2. deterministic rename rule
5. Policy must be explicitly documented in README and CLI help notes.

## Public Interface Impact
1. Runtime behavior becomes consistent and safer.
2. Optional future enhancement may add `--dry-run`, but this spec does not require it.

## Implementation Guidance
1. Create one selection pipeline used by both traversal modes.
2. Keep logic side-effect free until move phase.
3. Separate discover-eligible-files from execute-moves for testability.
4. Ensure conflict and skip reporting is human-readable.

## Engineering Tasks
1. Replace mode-specific filtering branches with a shared file-eligibility function.
2. Apply the same exclusion and extension checks for both traversal modes.
3. Add strict depth gate for recursive traversal.
4. Implement deterministic collision handling with clear user message.
5. Keep move behavior safe: no overwrite by default.

## Test Plan
1. Fixture tests for:
   1. hidden files
   2. excluded config/workspace files
   3. normal files with common extensions
   4. nested directories and depth boundaries
   5. destination filename collisions
2. Cross-mode parity test:
   1. identical policy outcomes for recursive vs non-recursive when scope overlaps.
3. Regression test proving no bypass of exclusion policy in recursive mode.

## Acceptance Criteria
1. No policy drift between traversal modes.
2. Collision behavior is deterministic and tested.
3. File safety behavior is documented and matches tests.
4. No unexpected moves in standard fixture scenarios.

## Risks
1. Behavior changes may surprise users relying on prior inconsistent behavior.
2. Broad exclusion patterns can accidentally filter desired files if not precise.

## Rollout
1. Release with explicit safety behavior normalization note.
2. Provide before/after examples in changelog.

## Implementation Status
Status: completed on 2026-03-06

Implemented decisions:
1. Both non-recursive and recursive modes now use the same shared discovery pipeline.
2. Eligibility policy is identical across modes:
   1. dotfiles are skipped
   2. exact-name exclusions are skipped
   3. suffix-based exclusions are skipped where configured
   4. files without an extension are skipped
   5. multi-extension files are categorized by their final suffix
3. Recursive traversal enforces the configured depth boundary before eligibility is applied.
4. Move conflicts never overwrite an existing destination file.
5. Traversal order is stable so same-run source collisions resolve deterministically and skipped files are reported clearly.

Validation completed:
1. Added cross-mode parity coverage for overlapping scope.
2. Added deterministic recursive collision coverage.
3. Added multi-extension coverage.
4. Verified README and CLI help both document the locked safety policy.
5. Ran the full test suite successfully.
