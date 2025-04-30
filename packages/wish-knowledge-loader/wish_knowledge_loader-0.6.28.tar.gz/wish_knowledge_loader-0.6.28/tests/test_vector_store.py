"""Tests for vector store functionality."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from langchain.schema import Document
from wish_models.settings import Settings

from wish_knowledge_loader.nodes.vector_store import VectorStore


class TestVectorStore:
    """Test for VectorStore."""

    @pytest.fixture
    def settings(self):
        """Create test settings."""
        settings = MagicMock(spec=Settings)
        settings.OPENAI_API_KEY = "test-api-key"
        settings.OPENAI_MODEL = "text-embedding-3-small"
        settings.OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
        settings.db_dir = Path("/tmp/db")
        return settings

    @patch("wish_knowledge_loader.nodes.vector_store.OpenAIEmbeddings")
    @patch("wish_knowledge_loader.nodes.vector_store.Chroma")
    @patch("wish_knowledge_loader.nodes.vector_store.Settings", return_value=MagicMock())
    def test_store(self, mock_settings_class, mock_chroma, mock_embeddings, settings):
        """Test storing documents in a vector store."""
        # Set up mock settings
        mock_settings = mock_settings_class.return_value
        mock_settings.OPENAI_API_KEY = settings.OPENAI_API_KEY
        mock_settings.OPENAI_MODEL = settings.OPENAI_MODEL
        mock_settings.db_dir = settings.db_dir

        # Create VectorStore instance
        vector_store = VectorStore(settings)

        # Set up mocks
        mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = mock_embeddings_instance

        mock_vectorstore = MagicMock()
        mock_chroma.from_documents.return_value = mock_vectorstore

        # Create test documents
        documents = [
            Document(page_content="Test content 1", metadata={"source": "test1.md"}),
            Document(page_content="Test content 2", metadata={"source": "test2.md"})
        ]

        # Call store method
        title = "Test Knowledge"
        vector_store.store(title, documents)

        # Check if OpenAIEmbeddings was created with correct arguments
        mock_embeddings.assert_called_once_with(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_EMBEDDING_MODEL,
            disallowed_special=()
        )

        # Check if Chroma.from_documents was called with correct arguments
        mock_chroma.from_documents.assert_called_once_with(
            documents=documents,
            embedding=vector_store.embeddings,
            persist_directory=str(settings.db_dir / title)
        )
