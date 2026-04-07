"""Tests for configuration module."""
import os
import pytest
from unittest.mock import patch


class TestSettings:
    """Test cases for Settings dataclass."""

    @patch('llms.config.load_dotenv')
    @patch.dict(
        os.environ,
        {
            'GROQ_API_KEY': 'test-api-key',
            'MODEL_NAME': 'test-model',
            'TEMPERATURE': '0.5',
            'STREAMING': 'false',
            'POSTGRES_URL': 'postgresql://postgres:postgres@localhost:5432/projectsmith',
            'FAST_API': 'http://localhost:8000',
        },
        clear=True,
    )
    def test_load_settings_with_all_env_vars(self, mock_load_dotenv):
        """Test loading settings with all environment variables set."""
        from llms.config import Settings

        settings = Settings.load()

        assert settings.GROQ_API_KEY == 'test-api-key'
        assert settings.MODEL_NAME == 'test-model'
        assert settings.TEMPERATURE == 0.5
        assert settings.STREAMING is False
        assert settings.POSTGRES_URL == 'postgresql://postgres:postgres@localhost:5432/projectsmith'

    @patch('llms.config.load_dotenv')
    @patch.dict(
        os.environ,
        {
            'GROQ_API_KEY': 'test-api-key',
            'POSTGRES_URL': 'postgresql://postgres:postgres@localhost:5432/projectsmith',
            'FAST_API': 'http://localhost:8000',
        },
        clear=True,
    )
    def test_load_settings_with_defaults(self, mock_load_dotenv):
        """Test loading settings with only required env var set."""
        from llms.config import Settings

        settings = Settings.load()

        assert settings.GROQ_API_KEY == 'test-api-key'
        assert settings.MODEL_NAME == 'llama-3.3-70b-versatile'
        assert settings.TEMPERATURE == 0.7
        assert settings.STREAMING is True
        assert settings.POSTGRES_URL == 'postgresql://postgres:postgres@localhost:5432/projectsmith'

    @patch('llms.config.load_dotenv')
    @patch.dict(os.environ, {}, clear=True)
    def test_load_settings_missing_api_key(self, mock_load_dotenv):
        """Test that ValueError is raised when GROQ_API_KEY is missing."""
        from llms.config import Settings

        with pytest.raises(ValueError, match="GROQ_API_KEY is missing"):
            Settings.load()

    @patch('llms.config.load_dotenv')
    @patch.dict(
        os.environ,
        {
            'GROQ_API_KEY': 'test-key',
            'POSTGRES_URL': 'postgresql://postgres:postgres@localhost:5432/projectsmith',
            'FAST_API': 'http://localhost:8000',
            'STREAMING': 'True',
        },
        clear=True,
    )
    def test_streaming_case_insensitive_true(self, mock_load_dotenv):
        """Test that streaming=True works with different cases."""
        from llms.config import Settings

        settings = Settings.load()
        assert settings.STREAMING is True

    @patch('llms.config.load_dotenv')
    @patch.dict(
        os.environ,
        {
            'GROQ_API_KEY': 'test-key',
            'POSTGRES_URL': 'postgresql://postgres:postgres@localhost:5432/projectsmith',
            'FAST_API': 'http://localhost:8000',
            'STREAMING': 'False',
        },
        clear=True,
    )
    def test_streaming_case_insensitive_false(self, mock_load_dotenv):
        """Test that streaming=False works with different cases."""
        from llms.config import Settings

        settings = Settings.load()
        assert settings.STREAMING is False
