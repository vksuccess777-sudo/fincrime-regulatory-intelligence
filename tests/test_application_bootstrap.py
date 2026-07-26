from src.bootstrap.application_bootstrap import (
    ApplicationBootstrap,
)

from src.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)

from src.llm.groq_provider import GroqProvider

from src.prompts.prompt_builder import PromptBuilder

from src.rag.context_builder import ContextBuilder

from src.retrieval.retrieval_engine import (
    RetrievalEngine,
)

from src.services.question_answering_service import (
    QuestionAnsweringService,
)

from src.vectorstore.chroma_vector_store import (
    ChromaVectorStore,
)


def test_bootstrap_can_be_created():

    bootstrap = ApplicationBootstrap()

    assert bootstrap is not None


def test_embedding_provider_created():

    bootstrap = ApplicationBootstrap()

    provider = bootstrap.embedding_provider()

    assert isinstance(
        provider,
        SentenceTransformerProvider,
    )


def test_embedding_provider_is_singleton():

    bootstrap = ApplicationBootstrap()

    first = bootstrap.embedding_provider()

    second = bootstrap.embedding_provider()

    assert first is second


def test_vector_store_created():

    bootstrap = ApplicationBootstrap()

    store = bootstrap.vector_store()

    assert isinstance(
        store,
        ChromaVectorStore,
    )


def test_vector_store_is_singleton():

    bootstrap = ApplicationBootstrap()

    first = bootstrap.vector_store()

    second = bootstrap.vector_store()

    assert first is second


def test_retrieval_engine_created():

    bootstrap = ApplicationBootstrap()

    retrieval = bootstrap.retrieval_engine()

    assert isinstance(
        retrieval,
        RetrievalEngine,
    )


def test_retrieval_engine_is_singleton():

    bootstrap = ApplicationBootstrap()

    first = bootstrap.retrieval_engine()

    second = bootstrap.retrieval_engine()

    assert first is second


def test_context_builder_created():

    bootstrap = ApplicationBootstrap()

    assert isinstance(
        bootstrap.context_builder(),
        ContextBuilder,
    )


def test_prompt_builder_created():

    bootstrap = ApplicationBootstrap()

    assert isinstance(
        bootstrap.prompt_builder(),
        PromptBuilder,
    )


def test_llm_provider_created():

    bootstrap = ApplicationBootstrap()

    assert isinstance(
        bootstrap.llm_provider(),
        GroqProvider,
    )


def test_question_answering_service_created():

    bootstrap = ApplicationBootstrap()

    qa = bootstrap.question_answering_service()

    assert isinstance(
        qa,
        QuestionAnsweringService,
    )


def test_question_answering_service_is_singleton():

    bootstrap = ApplicationBootstrap()

    first = bootstrap.question_answering_service()

    second = bootstrap.question_answering_service()

    assert first is second