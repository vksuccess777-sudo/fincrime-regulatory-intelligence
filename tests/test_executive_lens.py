from src.prompts.executive_lens import ExecutiveLens


def test_returns_string():
    lens = ExecutiveLens()

    result = lens.build()

    assert isinstance(result, str)


def test_not_empty():
    lens = ExecutiveLens()

    result = lens.build()

    assert result


def test_contains_board():
    lens = ExecutiveLens()

    result = lens.build()

    assert "board" in result.lower()


def test_contains_governance():
    lens = ExecutiveLens()

    result = lens.build()

    assert "governance" in result.lower()


def test_contains_management():
    lens = ExecutiveLens()

    result = lens.build()

    assert "management" in result.lower()


def test_contains_business():
    lens = ExecutiveLens()

    result = lens.build()

    assert "business" in result.lower()


def test_contains_reputational():
    lens = ExecutiveLens()

    result = lens.build()

    assert "reputational" in result.lower()