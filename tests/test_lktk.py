from lktk.parser import lkml_parser
import pytest


@pytest.mark.parametrize(
    "input_,output",
    [
        (
            '',
            """lkml
""",
        ),
        # comment
        (
            '# this is comment',
            """lkml
""",
        ),
        # ===== composite termination =====
        # pair
        (
            'project_name: "my project name"',
            """lkml
    pair
        project_name
        "my project name"
""",
        ),
        (
            'key1: "value1" key2: "value2"',
            """lkml
    pair
        key1
        "value1"
    pair
        key2
        "value2"
""",
        ),
        # yesno
        (
            'yes_no: yes',
            """lkml
    pair
        yes_no
        yes
""",
        ),
        # arr
        (
            'values: []',
            """lkml
    pair
        values
        arr\tNone
""",
        ),
        (
            'values: ["value1", "value2"]',
            """lkml
    pair
        values
        arr
            "value1"
            "value2"
""",
        ),
        # dict
        (
            '''dictionary: {}''',
            """lkml
    pair
        dictionary
        dict\tNone
""",
        ),
        (
            '''dictionary: {
  key: "value"
}''',
            """lkml
    pair
        dictionary
        dict
            pair
                key
                "value"
""",
        ),
        # named_dict
        (
            '''named_dictionary: name {
  key: "value"
}''',
            """lkml
    pair
        named_dictionary
        named_dict
            name
            dict
                pair
                    key
                    "value"
""",
        ),
        # ===== simple termination =====
        # string
        (
            'key: "value # not comment"',
            """lkml
    pair
        key
        "value # not comment"
""",
        ),
        # codeblock
        (
            'expression: #this is code block ;;',
            """lkml
    pair
        expression
        #this is code block
""",
        ),
        (
            'sql: code block 1;; sql_xxx: code block 2;;',
            """lkml
    pair
        sql
        code block 1
    pair
        sql_xxx
        code block 2
""",
        ),
        # number
        (
            'num: 3.14',
            """lkml
    pair
        num
        3.14
""",
        ),
    ],
)
def test_dummy(input_: str, output: str) -> None:
    tree = lkml_parser.parse(input_)
    assert tree.pretty(indent_str=" " * 4) == output
