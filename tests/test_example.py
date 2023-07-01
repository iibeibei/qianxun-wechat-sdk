def add_numbers(x, y):
    return x + y


def test_add_numbers():
    assert add_numbers(2, 3) == 5


def test_add_numbers_negative():
    assert add_numbers(-2, -3) == -5


def test_add_numbers_zero():
    assert add_numbers(0, 0) == 0


if __name__ == "__main__":
    pass
