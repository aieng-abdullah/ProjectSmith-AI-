"""Pytest configuration and fixtures."""
import pytest
from unittest.mock import Mock, patch


@pytest.fixture
def mock_settings():
    """Fixture providing mocked settings."""
    with patch('llms.config.settings') as mock:
        mock.GROQ_API_KEY = 'test-api-key'
        mock.MODEL_NAME = 'test-model'
        mock.TEMPERATURE = 0.7
        mock.STREAMING = True
        yield mock


@pytest.fixture
def mock_chat_groq():
    """Fixture providing mocked ChatGroq."""
    with patch('llms.model.ChatGroq') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock
