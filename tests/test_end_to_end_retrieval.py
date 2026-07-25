"""
End-to-End Retrieval Test

Sprint:
    Sprint 6 - D5

Verifies the complete indexing and retrieval pipeline using the
MockEmbeddingProvider.
"""

from src.embeddings.mock_embedding_provider import MockEmbeddingProvider
from src.indexing.index_builder import IndexBuilder
from src.processing.document_chunk import DocumentChunk
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.vectorstore.mock_vector_store import MockVectorStore


def test_end_to_end_semantic_retrieval():
    provider = MockEmbeddingProvider()
    store = MockVectorStore()

    builder = IndexBuilder(
        embedding_provider=provider,
        vector_store=store,
    )

    chunks = [
        DocumentChunk(
            chunk_id="1",
            text="Enhanced Due Diligence is required for higher-risk customers.",
            page_start=1,
            page_end=1,
            section_title="Recommendation 10",
            metadata={"source": "FATF"},
        ),
        DocumentChunk(
            chunk_id="2",
            text="Suspicious Activity Reports must be filed promptly.",
            page_start=2,
            page_end=2,
            section_title="Recommendation 20",
            metadata={"source": "FATF"},
        ),
        DocumentChunk(
            chunk_id="3",
            text="Banks should maintain a documented customer risk assessment.",
            page_start=3,
            page_end=3,
            section_title="Customer Risk Assessment",
            metadata={"source": "FCA"},
        ),
    ]

    builder.index_chunks(chunks)

    pipeline = RetrievalPipeline(
        embedding_provider=provider,
        vector_store=store,
    )

    results = pipeline.search(
        question="What is Enhanced Due Diligence?",
        k=2,
    )

    # Pipeline executed successfully
    assert len(results) == 2

    # Returned objects are EmbeddingResult instances
    assert all(result.chunk_id for result in results)

    # Embeddings have expected dimensionality
    assert all(result.dimension == provider.dimension for result in results)

    # Metadata from the provider is preserved
    assert all("provider" in result.metadata for result in results)