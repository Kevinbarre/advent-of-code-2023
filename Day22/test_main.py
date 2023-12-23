import pytest

from main import part1, part2, parse_bricks, Brick, sort_bricks_vertically, fall_brick, settle_bricks, \
    get_destructible_bricks, count_supported_bricks, count_supported_brick

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 5


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 7


def test_parse_bricks():
    # Given
    lines = ["1,0,1~1,2,1",
             "0,0,2~2,0,2",
             "0,2,3~2,2,3",
             "0,0,4~0,2,4",
             "2,0,5~2,2,5",
             "0,1,6~2,1,6",
             "1,1,8~1,1,9"]
    # When
    result = parse_bricks(lines)
    # Then
    assert result == [Brick((1, 0, 1), (1, 2, 1)),
                      Brick((0, 0, 2), (2, 0, 2)),
                      Brick((0, 2, 3), (2, 2, 3)),
                      Brick((0, 0, 4), (0, 2, 4)),
                      Brick((2, 0, 5), (2, 2, 5)),
                      Brick((0, 1, 6), (2, 1, 6)),
                      Brick((1, 1, 8), (1, 1, 9))]


def test_sort_bricks():
    # Given
    bricks = [Brick((0, 1, 8), (0, 2, 8)),
              Brick((0, 0, 3), (0, 1, 3)),
              Brick((0, 0, 8), (0, 0, 9)),
              Brick((1, 0, 1), (1, 2, 1))]
    # When
    result = sort_bricks_vertically(bricks)
    # Then
    assert result == [Brick((1, 0, 1), (1, 2, 1)),
                      Brick((0, 0, 3), (0, 1, 3)),
                      Brick((0, 0, 8), (0, 0, 9)),
                      Brick((0, 1, 8), (0, 2, 8))]


def test_fall_brick_on_ground():
    # Given
    brick = Brick((1, 0, 1), (1, 2, 1))
    # When
    result = fall_brick(brick, [])
    # Then
    assert result == [Brick((1, 0, 1), (1, 2, 1))]


def test_fall_brick_above_ground():
    # Given
    brick = Brick((1, 0, 2), (1, 2, 2))
    # When
    result = fall_brick(brick, [])
    # Then
    assert result == [Brick((1, 0, 1), (1, 2, 1))]


def test_fall_brick_on_other_brick_on_ground():
    # Given
    brick = Brick((1, 0, 3), (1, 2, 3))
    brick_on_ground = Brick((0, 1, 1), (2, 1, 1))  # Perpendicular brick
    # When
    result = fall_brick(brick, [brick_on_ground])
    # Then
    assert result == [brick_on_ground, Brick((1, 0, 2), (1, 2, 2))]
    fallen_brick = result[1]
    assert fallen_brick in brick_on_ground.supported_bricks
    assert brick_on_ground in fallen_brick.supported_by


def test_fall_brick_with_other_brick_not_below():
    # Given
    brick = Brick((1, 0, 3), (1, 2, 3))
    brick_on_ground = Brick((0, 0, 1), (0, 2, 1))  # Parallel brick
    # When
    result = fall_brick(brick, [brick_on_ground])
    # Then
    assert result == [brick_on_ground, Brick((1, 0, 1), (1, 2, 1))]
    fallen_brick = result[1]
    assert fallen_brick not in brick_on_ground.supported_bricks
    assert brick_on_ground not in fallen_brick.supported_by


@pytest.mark.parametrize("brick_1, brick_2, expected", [
    # Single cube bricks are same position
    (Brick((1, 1, 1), (1, 1, 1)), Brick((1, 1, 1), (1, 1, 1)), True),
    # Brick above the other
    (Brick((1, 1, 1), (1, 1, 1)), Brick((1, 2, 1), (1, 2, 1)), False),
    # Brick right to the other
    (Brick((1, 1, 1), (1, 1, 1)), Brick((2, 1, 1), (2, 1, 1)), False),
    # Brick below the other
    (Brick((1, 1, 1), (1, 1, 1)), Brick((1, 0, 1), (1, 0, 1)), False),
    # Brick left to the other
    (Brick((1, 1, 1), (1, 1, 1)), Brick((0, 1, 1), (0, 1, 1)), False),
    # Parallel vertical bricks
    (Brick((0, 0, 1), (0, 2, 1)), Brick((1, 0, 1), (1, 2, 1)), False),
    # Parallel horizontal bricks
    (Brick((0, 0, 1), (2, 0, 1)), Brick((0, 1, 1), (2, 1, 1)), False),
    # Perpendicular bricks
    (Brick((0, 1, 1), (2, 1, 1)), Brick((1, 0, 1), (1, 2, 1)), True),
])
def test_brick_collide(brick_1, brick_2, expected):
    # Given
    # When
    result = brick_1.collide(brick_2)
    # Then
    assert result is expected


def test_settle_bricks():
    # Given
    bricks = [Brick((1, 0, 1), (1, 2, 1)),
              Brick((0, 0, 2), (2, 0, 2)),
              Brick((0, 2, 3), (2, 2, 3)),
              Brick((0, 0, 4), (0, 2, 4)),
              Brick((2, 0, 5), (2, 2, 5)),
              Brick((0, 1, 6), (2, 1, 6)),
              Brick((1, 1, 8), (1, 1, 9))]
    # When
    settled_bricks = settle_bricks(bricks)
    # Then
    assert settled_bricks == [Brick((1, 0, 1), (1, 2, 1)),
                              Brick((0, 0, 2), (2, 0, 2)),
                              Brick((0, 2, 2), (2, 2, 2)),
                              Brick((0, 0, 3), (0, 2, 3)),
                              Brick((2, 0, 3), (2, 2, 3)),
                              Brick((0, 1, 4), (2, 1, 4)),
                              Brick((1, 1, 5), (1, 1, 6))]
    a = settled_bricks[0]
    b = settled_bricks[1]
    c = settled_bricks[2]
    d = settled_bricks[3]
    e = settled_bricks[4]
    f = settled_bricks[5]
    g = settled_bricks[6]
    assert settled_bricks == [a, b, c, d, e, f, g]
    # Supported bricks
    assert a.supported_bricks == {b, c}
    assert b.supported_bricks == {d, e}
    assert c.supported_bricks == {d, e}
    assert d.supported_bricks == {f}
    assert e.supported_bricks == {f}
    assert f.supported_bricks == {g}
    assert g.supported_bricks == set()
    # Supported by
    assert a.supported_by == set()
    assert b.supported_by == {a}
    assert c.supported_by == {a}
    assert d.supported_by == {b, c}
    assert e.supported_by == {b, c}
    assert f.supported_by == {d, e}
    assert g.supported_by == {f}


def test_get_destructible_bricks():
    # Given
    a = Brick((1, 0, 1), (1, 2, 1))
    b = Brick((0, 0, 2), (2, 0, 2))
    c = Brick((0, 2, 2), (2, 2, 2))
    d = Brick((0, 0, 3), (0, 2, 3))
    e = Brick((2, 0, 3), (2, 2, 3))
    f = Brick((0, 1, 4), (2, 1, 4))
    g = Brick((1, 1, 5), (1, 1, 6))
    # Supported bricks
    a.supported_bricks = {b, c}
    b.supported_bricks = {d, e}
    c.supported_bricks = {d, e}
    d.supported_bricks = {f}
    e.supported_bricks = {f}
    f.supported_bricks = {g}
    g.supported_bricks = set()
    # Supported by
    a.supported_by = set()
    b.supported_by = {a}
    c.supported_by = {a}
    d.supported_by = {b, c}
    e.supported_by = {b, c}
    f.supported_by = {d, e}
    g.supported_by = {f}
    settled_bricks = [a, b, c, d, e, f, g]
    # When
    result = get_destructible_bricks(settled_bricks)
    # Then
    assert result == {b, c, d, e, g}


def test_count_supported_bricks():
    # Given
    a = Brick((1, 0, 1), (1, 2, 1))
    b = Brick((0, 0, 2), (2, 0, 2))
    c = Brick((0, 2, 2), (2, 2, 2))
    d = Brick((0, 0, 3), (0, 2, 3))
    e = Brick((2, 0, 3), (2, 2, 3))
    f = Brick((0, 1, 4), (2, 1, 4))
    g = Brick((1, 1, 5), (1, 1, 6))
    # Supported bricks
    a.supported_bricks = {b, c}
    b.supported_bricks = {d, e}
    c.supported_bricks = {d, e}
    d.supported_bricks = {f}
    e.supported_bricks = {f}
    f.supported_bricks = {g}
    g.supported_bricks = set()
    # Supported by
    a.supported_by = set()
    b.supported_by = {a}
    c.supported_by = {a}
    d.supported_by = {b, c}
    e.supported_by = {b, c}
    f.supported_by = {d, e}
    g.supported_by = {f}
    settled_bricks = [a, b, c, d, e, f, g]
    # When
    result = count_supported_bricks(settled_bricks)
    # Then
    assert result == {
        a: 6,
        b: 0,
        c: 0,
        d: 0,
        e: 0,
        f: 1,
        g: 0
    }


@pytest.mark.parametrize("test_input, expected", [("a", 6), ("b", 0), ("c", 0), ("d", 0), ("e", 0), ("f", 1), ("g", 0)])
def test_count_supported_brick(test_input, expected):
    # Given
    a = Brick((1, 0, 1), (1, 2, 1))
    b = Brick((0, 0, 2), (2, 0, 2))
    c = Brick((0, 2, 2), (2, 2, 2))
    d = Brick((0, 0, 3), (0, 2, 3))
    e = Brick((2, 0, 3), (2, 2, 3))
    f = Brick((0, 1, 4), (2, 1, 4))
    g = Brick((1, 1, 5), (1, 1, 6))
    # Supported bricks
    a.supported_bricks = {b, c}
    b.supported_bricks = {d, e}
    c.supported_bricks = {d, e}
    d.supported_bricks = {f}
    e.supported_bricks = {f}
    f.supported_bricks = {g}
    g.supported_bricks = set()
    # Supported by
    a.supported_by = set()
    b.supported_by = {a}
    c.supported_by = {a}
    d.supported_by = {b, c}
    e.supported_by = {b, c}
    f.supported_by = {d, e}
    g.supported_by = {f}
    bricks_by_name = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g}
    # When
    result = count_supported_brick(bricks_by_name[test_input])
    # Then
    assert result == expected


def test_something():
    assert set().issubset(set())
