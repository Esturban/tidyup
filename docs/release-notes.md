# Release Notes

## Unreleased

### Packaging and runtime guarantees

- `import tidyup` no longer depends on `setuptools_scm` being available at runtime.
- `python -m tidyup -h` is supported in minimal environments after installation.
- GitHub release signing uses a current Sigstore action so tagged releases no longer fail on deprecated artifact actions.

### Documentation and test guarantees

- README usage examples and help text are treated as regression-tested CLI contract.
- Parser, packaging, docs, and filesystem behavior coverage are split into focused test modules for easier diagnosis.
