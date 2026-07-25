"""
Tests for PromptBuilder.

Sprint:
    Sprint 7 - D3
"""

from src.prompts.prompt_builder import PromptBuilder


def test_prompt_contains_system_prompt():
    builder = PromptBuilder()

    prompt = builder.build(
        question="What is Enhanced Due Diligence?",
        context="Example Context",
    )

    assert "Financial Crime Regulatory Intelligence Assistant" in prompt


def test_prompt_contains_context():
    builder = PromptBuilder()

    prompt = builder.build(
        question="Question",
        context="Context Text",
    )

    assert "Context Text" in prompt


def test_prompt_contains_question():
    builder = PromptBuilder()

    question = "What is Recommendation 10?"

    prompt = builder.build(
        question=question,
        context="Context",
    )

    assert question in prompt


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

    assert "Question" in prompt
    assert "REGULATORY CONTEXT" in prompt


def test_empty_question():
    builder = PromptBuilder()

    prompt = builder.build(
        question="",
        context="Context",
    )

    assert "Context" in prompt
    assert "USER QUESTION" in prompt


def test_prompt_contains_llm_rules():
    builder = PromptBuilder()

    prompt = builder.build(
        question="Question",
        context="Context",
    )

    assert "Answer ONLY using the supplied regulatory context." in prompt
    assert "Never invent regulations." in prompt
    assert "Never fabricate citations." in prompt