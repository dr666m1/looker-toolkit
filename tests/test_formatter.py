import pytest

from lktk.parser import lkml_parser, comments
from lktk.formatter import LkmlFormatter


@pytest.mark.parametrize(
    "input_, output",
    [
        ("", ""),
        (
            """key1: value1 key2: 3.14""",
            """\
key1: value1
key2: 3.14""",
        ),
        # ident
        (
            """key1: parent . child key2: value *""",
            """\
key1: parent.child
key2: value*""",
        ),
        # arr
        (
            """values: []""",
            """values: []""",
        ),
        (
            """values: [ value ]""",
            """values: [ value ]""",
        ),
        (
            """values: [ value1, value2, [value3, value4], [value5] ]""",
            """values: [
  value1,
  value2,
  [
    value3,
    value4
  ],
  [ value5 ]
]""",
        ),
        # code block
        (
            """sql: code block ;;""",
            """sql: code block ;;""",
        ),
        (
            """\
sql: code
block ;;""",
            """\
sql:
  code
  block
;;""",
        ),
        # dict
        (
            """dict: {}""",
            """dict: {}""",
        ),
        (
            """dict: { key: value }""",
            """dict: {
  key: value
}""",
        ),
        (
            """dict: {
  key1: {key2: value2 key3: value3}
}""",
            """\
dict: {
  key1: {
    key2: value2
    key3: value3
  }
}""",
        ),
        # named dict
        (
            """dict: ident {
  key1: ident1 {}
  key2: ident2 { key3: ident3 { } }
}""",
            """\
dict: ident {
  key1: ident1 {}
  key2: ident2 {
    key3: ident3 {}
  }
}""",
        ),
        # leading comments
        ("# eof", "# eof"),
        (
            """\
# comment 1
key1: value1
# comment 2.1
# comment 2.2
key2: value2""",
            """\
# comment 1
key1: value1
# comment 2.1
# comment 2.2
key2: value2""",
        ),
        (
            """\
# comment a
sql_a: code a ;;
# comment b.1
# comment b.2
sql_b: code b ;;""",
            """\
# comment a
sql_a: code a ;;
# comment b.1
# comment b.2
sql_b: code b ;;""",
        ),
        (
            """\
# comment 
key: value""",  # noqa: W291
            """\
# comment
key: value""",
        ),
        (
            """\
key: [
  # this is comment
  ident
]""",
            """\
key: [
  # this is comment
  ident
]""",
        ),
        # trailing comments
        ("key: value # comment", "key: value # comment"),
        ("""\
key: { # comment
  key: pair
}""", """\
key: { # comment
  key: pair
}"""),
    ],
)
def test_formatter(input_: str, output: str) -> None:
    # once formatted text matches expected output
    tree1 = lkml_parser.parse(input_)
    text1 = LkmlFormatter(tree1, comments).print()
    assert text1 == output

    # twice formatted text also matches expected output
    tree2 = lkml_parser.parse(text1)
    text2 = LkmlFormatter(tree2, comments).print()
    assert text2 == output
