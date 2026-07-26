from src.prompts.control_lens import ControlLens


def test_returns_string():
    lens = ControlLens()

    result = lens.build()

    assert isinstance(result, str)


def test_not_empty():
    lens = ControlLens()

    result = lens.build()

    assert result


def test_contains_control():
    lens = ControlLens()

    result = lens.build()

    assert "control" in result.lower()


def test_contains_preventive():
    lens = ControlLens()

    result = lens.build()

    assert "preventive" in result.lower()


def test_contains_detective():
    lens = ControlLens()

    result = lens.build()

    assert "detective" in result.lower()


def test_contains_design_effectiveness():
    lens = ControlLens()

    result = lens.build()

    assert "design effectiveness" in result.lower()


def test_contains_operating_effectiveness():
    lens = ControlLens()

    result = lens.build()

    assert "operating effectiveness" in result.lower()