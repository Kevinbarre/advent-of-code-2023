from main import part1, part2, parse_game, Set, Game, is_set_possible, is_game_possible

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.readlines()
    # When
    result = part1(lines)
    # Then
    assert result == 8


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.readlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


def test_parse_game():
    # Given
    raw_game = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    # When
    game = parse_game(raw_game)
    # Then
    assert game.id == 1
    assert len(game.sets) == 3
    assert game.sets[0].red == 4
    assert game.sets[0].green == 0
    assert game.sets[0].blue == 3
    assert game.sets[1].red == 1
    assert game.sets[1].green == 2
    assert game.sets[1].blue == 6
    assert game.sets[2].red == 0
    assert game.sets[2].green == 2
    assert game.sets[2].blue == 0


def test_is_set_possible_true():
    # Given
    set1 = Set()
    set1.green = 4
    set1.blue = 3
    # When
    result = is_set_possible(set1)
    # Then
    assert result is True


def test_is_set_possible_false():
    # Given
    set1 = Set()
    set1.red = 20
    set1.green = 8
    set1.blue = 6
    # When
    result = is_set_possible(set1)
    # Then
    assert result is False


def test_is_game_possible_true():
    # Given
    set1 = Set()
    set1.red = 4
    set1.blue = 3
    set2 = Set()
    set2.red = 1
    set2.green = 2
    set2.blue = 6
    set3 = Set()
    set3.green = 2
    game = Game(1, [set1, set2, set3])
    # When
    result = is_game_possible(game)
    # Then
    assert result is True


def test_is_game_possible_false():
    # Given
    set1 = Set()
    set1.red = 20
    set1.green = 8
    set1.blue = 6
    set2 = Set()
    set2.red = 4
    set2.green = 13
    set2.blue = 5
    set3 = Set()
    set3.red = 1
    set3.green = 5
    game = Game(1, [set1, set2, set3])
    # When
    result = is_game_possible(game)
    # Then
    assert result is False
