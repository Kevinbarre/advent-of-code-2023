from networkx import Graph
from networkx.utils import graphs_equal

from main import part1, part2, parse_graph, get_separate_groups

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 54


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


def test_parse_graph():
    # Given
    lines = ["jqt: rhn xhk nvd",
             "rsh: frs pzl lsr",
             "xhk: hfx",
             "cmg: qnr nvd lhk bvb",
             "rhn: xhk bvb hfx",
             "bvb: xhk hfx",
             "pzl: lsr hfx nvd",
             "qnr: nvd",
             "ntq: jqt hfx bvb xhk",
             "nvd: lhk",
             "lsr: lhk",
             "rzs: qnr cmg lsr rsh",
             "frs: qnr lhk lsr"]
    expected = Graph()
    expected.add_nodes_from(
        {"jqt", "rhn", "xhk", "nvd", "rsh", "frs", "pzl", "lsr", "hfx", "cmg", "qnr", "lhk", "bvb", "ntq",
         "rzs"})
    expected.add_edges_from(
        [("jqt", "rhn"), ("jqt", "xhk"), ("jqt", "nvd"), ("rsh", "frs"), ("rsh", "pzl"), ("rsh", "lsr"), ("xhk", "hfx"),
         ("cmg", "qnr"), ("cmg", "nvd"), ("cmg", "lhk"), ("cmg", "bvb"), ("rhn", "xhk"), ("rhn", "bvb"), ("rhn", "hfx"),
         ("bvb", "xhk"), ("bvb", "hfx"), ("pzl", "lsr"), ("pzl", "hfx"), ("pzl", "nvd"), ("qnr", "nvd"), ("ntq", "jqt"),
         ("ntq", "hfx"), ("ntq", "bvb"), ("ntq", "xhk"), ("nvd", "lhk"), ("lsr", "lhk"), ("rzs", "qnr"), ("rzs", "cmg"),
         ("rzs", "lsr"), ("rzs", "rsh"), ("frs", "qnr"), ("frs", "lhk"), ("frs", "lsr")])
    # When
    result = parse_graph(lines)
    # Then
    assert graphs_equal(result, expected)


def test_get_separate_groups():
    # Given
    graph = Graph()
    graph.add_nodes_from(
        {"jqt", "rhn", "xhk", "nvd", "rsh", "frs", "pzl", "lsr", "hfx", "cmg", "qnr", "lhk", "bvb", "ntq",
         "rzs"})
    graph.add_edges_from(
        [("jqt", "rhn"), ("jqt", "xhk"), ("jqt", "nvd"), ("rsh", "frs"), ("rsh", "pzl"), ("rsh", "lsr"), ("xhk", "hfx"),
         ("cmg", "qnr"), ("cmg", "nvd"), ("cmg", "lhk"), ("cmg", "bvb"), ("rhn", "xhk"), ("rhn", "bvb"), ("rhn", "hfx"),
         ("bvb", "xhk"), ("bvb", "hfx"), ("pzl", "lsr"), ("pzl", "hfx"), ("pzl", "nvd"), ("qnr", "nvd"), ("ntq", "jqt"),
         ("ntq", "hfx"), ("ntq", "bvb"), ("ntq", "xhk"), ("nvd", "lhk"), ("lsr", "lhk"), ("rzs", "qnr"), ("rzs", "cmg"),
         ("rzs", "lsr"), ("rzs", "rsh"), ("frs", "qnr"), ("frs", "lhk"), ("frs", "lsr")])
    # When
    first, second = get_separate_groups(graph)
    # Then
    assert first == {"cmg", "frs", "lhk", "lsr", "nvd", "pzl", "qnr", "rsh", "rzs"}
    assert second == {"bvb", "hfx", "jqt", "ntq", "rhn", "xhk"}
