# Release Checklist

- Run `python3 -m pytest -q`.
- Run `python3 -m tidyup -h` from a clean virtual environment after installing the package.
- Confirm [`README.md`](../README.md) usage examples still match the parser help output and recursive semantics.
- Confirm release notes mention the runtime version fallback guarantee and README/help synchronization guarantee.
