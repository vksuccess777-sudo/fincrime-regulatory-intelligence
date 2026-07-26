from src.prompts.risk_lens import RiskLens


def test_returns_string():
    lens = RiskLens()

    result = lens.build()

    assert isinstance(result, str)


def test_not_empty():
    lens = RiskLens()

    result = lens.build()

    assert result


def test_contains_risk():
    lens = RiskLens()

    result = lens.build()

    assert "risk" in result.lower()


def test_contains_money_laundering():
    lens = RiskLens()

    result = lens.build()

    assert "money laundering" in result.lower()


def test_contains_terrorist_financing():
    lens = RiskLens()

    result = lens.build()

    assert "terrorist financing" in result.lower()


def test_contains_sanctions():
    lens = RiskLens()

    result = lens.build()

    assert "sanctions" in result.lower()


def test_contains_risk_based():
    lens = RiskLens()

    result = lens.build()

    assert "risk-based" in result.lower()