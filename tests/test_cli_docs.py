from pathlib import Path

from tidyup.utils import README_USAGE, SAFETY_NOTES, USAGE_EXAMPLES, build_parser

README = Path(__file__).resolve().parents[1] / "README.md"


def test_help_includes_recursive_and_order_examples():
    help_text = build_parser().format_help()

    assert "-r, --rearrange" in help_text
    assert "-L DEPTH" in help_text or "-L, --depth" in help_text
    for command, _description in USAGE_EXAMPLES:
        assert command in help_text
    for note in SAFETY_NOTES:
        assert note in help_text


def test_readme_matches_supported_usage_contract():
    readme = README.read_text()

    assert README_USAGE in readme
    assert "-de` => `year/month/extension/file" in readme
    assert "-ed` => `extension/year/month/file" in readme
    assert "-r` without `-L` defaults to depth `2`" in readme
    assert "-L` without `-r` is invalid" in readme
    for command, _description in USAGE_EXAMPLES:
        assert command in readme
