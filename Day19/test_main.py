import pytest

from main import part1, part2, Part, parse_input, parse_raw_part, parse_raw_workflow, get_eval_workflow, process_part, \
    get_accepted_parts, get_part_value

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 19114


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


def test_parse_input():
    # Given
    lines = ["px{a<2006:qkq,m>2090:A,rfg}",
             "pv{a>1716:R,A}",
             "lnx{m>1548:A,A}",
             "rfg{s<537:gd,x>2440:R,A}",
             "qs{s>3448:A,lnx}",
             "qkq{x<1416:A,crn}",
             "crn{x>2662:A,R}",
             "in{s<1351:px,qqz}",
             "qqz{s>2770:qs,m<1801:hdj,R}",
             "gd{a>3333:R,R}",
             "hdj{m>838:A,pv}",
             "",
             "{x=787,m=2655,a=1222,s=2876}",
             "{x=1679,m=44,a=2067,s=496}",
             "{x=2036,m=264,a=79,s=2244}",
             "{x=2461,m=1339,a=466,s=291}",
             "{x=2127,m=1623,a=2188,s=1013}"]
    expected_workflows = {
        "px": lambda p: "qkq" if p.a < 2006 else "A" if p.m > 2090 else "rfg",
        "pv": lambda p: "R" if p.a > 1716 else "A",
        "lnx": lambda p: "A" if p.m > 1548 else "A",
        "rfg": lambda p: "gd" if p.s < 537 else "R" if p.x > 2440 else "A",
        "qs": lambda p: "A" if p.s > 3448 else "lnx",
        "qkq": lambda p: "A" if p.x < 1416 else "crn",
        "crn": lambda p: "A" if p.x > 2662 else "R",
        "in": lambda p: "px" if p.s < 1351 else "qqz",
        "qqz": lambda p: "qs" if p.s > 2770 else "hdj" if p.m < 1801 else "R",
        "gd": lambda p: "R" if p.a > 3333 else "R",
        "hdj": lambda p: "A" if p.m > 838 else "pv"
    }
    # When
    workflows, parts = parse_input(lines)
    # Then
    assert parts == [Part(787, 2655, 1222, 2876),
                     Part(1679, 44, 2067, 496),
                     Part(2036, 264, 79, 2244),
                     Part(2461, 1339, 466, 291),
                     Part(2127, 1623, 2188, 1013)]
    assert workflows.keys() == expected_workflows.keys()
    for name, workflow in workflows.items():
        assert workflow.__code__.co_code == expected_workflows[name].__code__.co_code


@pytest.mark.parametrize("test_input, expected", [("x=787", 787), ("m=2655", 2655), ("a=1222", 1222), ("s=2876", 2876)])
def test_parse_raw_part(test_input, expected):
    # Given
    # When
    result = parse_raw_part(test_input)
    # Assert
    assert result == expected


def test_parse_raw_workflow():
    # Given
    raw_workflow = "a<2006:qkq,m>2090:A,rfg"
    # When
    result = parse_raw_workflow(raw_workflow)
    # Then
    assert result.__code__.co_code == (lambda p: "qkq" if p.a < 2006 else "A" if p.m > 2090 else "rfg").__code__.co_code


def test_get_eval_workflow():
    # Given
    raw_workflow = "a<2006:qkq,m>2090:A,rfg"
    # When
    result = get_eval_workflow(raw_workflow)
    # Then
    assert result == 'lambda p: "qkq" if p.a < 2006 else "A" if p.m > 2090 else "rfg"'


@pytest.mark.parametrize("test_input, expected", [(Part(787, 2655, 1222, 2876), True),
                                                  (Part(1679, 44, 2067, 496), False),
                                                  (Part(2036, 264, 79, 2244), True),
                                                  (Part(2461, 1339, 466, 291), False),
                                                  (Part(2127, 1623, 2188, 1013), True)])
def test_process_part(test_input, expected):
    # Given
    workflows = {
        "px": lambda p: "qkq" if p.a < 2006 else "A" if p.m > 2090 else "rfg",
        "pv": lambda p: "R" if p.a > 1716 else "A",
        "lnx": lambda p: "A" if p.m > 1548 else "A",
        "rfg": lambda p: "gd" if p.s < 537 else "R" if p.x > 2440 else "A",
        "qs": lambda p: "A" if p.s > 3448 else "lnx",
        "qkq": lambda p: "A" if p.x < 1416 else "crn",
        "crn": lambda p: "A" if p.x > 2662 else "R",
        "in": lambda p: "px" if p.s < 1351 else "qqz",
        "qqz": lambda p: "qs" if p.s > 2770 else "hdj" if p.m < 1801 else "R",
        "gd": lambda p: "R" if p.a > 3333 else "R",
        "hdj": lambda p: "A" if p.m > 838 else "pv"
    }
    # When
    result = process_part(workflows, test_input)
    # Then
    assert result is expected


def test_get_accepted_parts():
    # Given
    workflows = {
        "px": lambda p: "qkq" if p.a < 2006 else "A" if p.m > 2090 else "rfg",
        "pv": lambda p: "R" if p.a > 1716 else "A",
        "lnx": lambda p: "A" if p.m > 1548 else "A",
        "rfg": lambda p: "gd" if p.s < 537 else "R" if p.x > 2440 else "A",
        "qs": lambda p: "A" if p.s > 3448 else "lnx",
        "qkq": lambda p: "A" if p.x < 1416 else "crn",
        "crn": lambda p: "A" if p.x > 2662 else "R",
        "in": lambda p: "px" if p.s < 1351 else "qqz",
        "qqz": lambda p: "qs" if p.s > 2770 else "hdj" if p.m < 1801 else "R",
        "gd": lambda p: "R" if p.a > 3333 else "R",
        "hdj": lambda p: "A" if p.m > 838 else "pv"
    }
    parts = [Part(787, 2655, 1222, 2876),
             Part(1679, 44, 2067, 496),
             Part(2036, 264, 79, 2244),
             Part(2461, 1339, 466, 291),
             Part(2127, 1623, 2188, 1013)]
    # When
    result = get_accepted_parts(workflows, parts)
    # Then
    assert result == [Part(787, 2655, 1222, 2876),
                      Part(2036, 264, 79, 2244),
                      Part(2127, 1623, 2188, 1013)]


@pytest.mark.parametrize("test_input, expected", [(Part(787, 2655, 1222, 2876), 7540),
                                                  (Part(2036, 264, 79, 2244), 4623),
                                                  (Part(2127, 1623, 2188, 1013), 6951)])
def test_get_part_value(test_input, expected):
    # Given
    # When
    result = get_part_value(test_input)
    # Then
    assert result == expected
