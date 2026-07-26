from src.prompts.prompt_builder import PromptBuilder


def test_prompt_contains_system_prompt():
    builder = PromptBuilder()

    prompt = builder.build(
        question="What is CDD?",
        context="Customer Due Diligence context.",
    )

    assert "Financial Crime Regulatory Intelligence Assistant" in prompt


def test_prompt_contains_context():
    builder = PromptBuilder()

    prompt = builder.build(
        question="Question",
        context="Example Context",
    )

    assert "Example Context" in prompt


def test_prompt_contains_question():
    builder = PromptBuilder()

    prompt = builder.build(
        question="Example Question",
        context="Context",
    )

    assert "Example Question" in prompt


def test_prompt_contains_answer_section():
    builder = PromptBuilder()

    prompt = builder.build(
        question="Question",
        context="Context",
    )

    assert "ANSWER" in prompt


def test_empty_context():
    builder = PromptBuilder()

    prompt = builder.build(
        question="Question",
        context="",
    )

    assert "RETRIEVED REGULATORY CONTEXT" in prompt


def test_empty_question():
    builder = PromptBuilder()

    prompt = builder.build(
        question="",
        context="Context",
    )

    assert "USER QUESTION" in prompt


def test_prompt_contains_llm_rules():
    builder = PromptBuilder()

    prompt = builder.build(
        question="Question",
        context="Context",
    )

    # Core evidence-based rules
    assert "Never invent regulations." in prompt
    assert "Never fabricate citations." in prompt
    assert "Never speculate." in prompt
    assert "retrieved context is insufficient" in prompt

    # Lens integration
    assert "AUDITOR LENS" in prompt
    assert "RISK LENS" in prompt
    assert "CONTROL LENS" in prompt
    assert "EXECUTIVE LENS" in prompt

    # Structured response
    assert "Regulatory Summary" in prompt
    assert "Financial Crime Risks" in prompt
    assert "Expected Controls" in prompt
    assert "Suggested Audit Procedures" in prompt
    assert "Executive Summary" in prompt
    assert "References" in prompt
    assert "Confidence" in prompt
    assert "Disclaimer" in prompt