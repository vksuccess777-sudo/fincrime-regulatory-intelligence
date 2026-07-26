from src.prompts.auditor_lens import AuditorLens


def test_returns_string():
    lens = AuditorLens()

    result = lens.build()

    assert isinstance(result, str)


def test_not_empty():
    lens = AuditorLens()

    result = lens.build()

    assert result


def test_contains_auditor():
    lens = AuditorLens()

    result = lens.build()

    assert "auditor" in result.lower()


def test_contains_controls():
    lens = AuditorLens()

    result = lens.build()

    assert "control" in result.lower()


def test_contains_risk():
    lens = AuditorLens()

    result = lens.build()

    assert "risk" in result.lower()


def test_contains_professional_judgement():
    lens = AuditorLens()

    result = lens.build()

    assert "professional judgement" in result.lower()


def test_contains_retrieved_evidence():
    lens = AuditorLens()

    result = lens.build()

    assert "retrieved evidence" in result.lower()