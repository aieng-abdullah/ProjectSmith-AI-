"""Tests for LLM model service."""
import os
import pytest
from unittest.mock import patch, MagicMock
from langchain_core.prompts import ChatPromptTemplate

TEST_ENV = {
    'GROQ_API_KEY': 'test-key',
    'POSTGRES_URL': 'postgresql://postgres:postgres@localhost:5432/projectsmith',
    'FAST_API': 'http://localhost:8000',
}


@patch.dict(os.environ, TEST_ENV, clear=True)
class TestLLMService:
    """Test cases for LLMService class."""

    @patch("llms.model.LLMService.build_chain", return_value=MagicMock())
    @patch("llms.model.settings")
    def test_init_with_valid_prompt_type(self, mock_settings, mock_build_chain):
        """Test LLMService initialization with valid prompt type."""
        mock_settings.GROQ_API_KEY = "test-key"
        mock_settings.MODEL_NAME = "test-model"
        mock_settings.TEMPERATURE = 0.7

        from llms.model import LLMService

        service = LLMService(prompt_type="advisor", streaming=True)

        assert service.prompt_type == "advisor"
        assert service.streaming is True
        assert service.chain is mock_build_chain.return_value

    def test_get_prompt_advisor(self):
        """Test getting advisor prompt."""
        from llms.model import LLMService

        service = object.__new__(LLMService)
        prompt = service.get_prompt("advisor")

        assert isinstance(prompt, ChatPromptTemplate)
        assert "startup advisor" in prompt.messages[0].prompt.template.lower()

    def test_get_prompt_chat(self):
        """Test getting chat prompt."""
        from llms.model import LLMService

        service = object.__new__(LLMService)
        prompt = service.get_prompt("chat")

        assert isinstance(prompt, ChatPromptTemplate)
        assert "projectsmith" in prompt.messages[0].prompt.template.lower()

    def test_get_prompt_planner(self):
        """Test getting planner prompt."""
        from llms.model import LLMService

        service = object.__new__(LLMService)
        prompt = service.get_prompt("planner")

        assert isinstance(prompt, ChatPromptTemplate)
        assert "phase 1 — build this first" in prompt.messages[0].prompt.template.lower()

    def test_get_prompt_invalid(self):
        """Test that invalid prompt type raises ValueError."""
        from llms.model import LLMService

        service = object.__new__(LLMService)

        with pytest.raises(ValueError, match="Invalid prompt type"):
            service.get_prompt("invalid")

    @patch("llms.model.ChatPromptTemplate.from_messages")
    @patch("llms.model.ChatGroq")
    @patch("llms.model.settings")
    def test_build_chain_creates_pipeline(self, mock_settings, mock_chat_groq, mock_from_messages):
        """Test that build_chain creates a proper pipeline."""
        mock_settings.GROQ_API_KEY = "test-key"
        mock_settings.MODEL_NAME = "test-model"
        mock_settings.TEMPERATURE = 0.7

        mock_llm_instance = MagicMock()
        mock_chat_groq.return_value = mock_llm_instance

        prompt_mock = MagicMock()
        intermediate = MagicMock()
        pipeline_mock = MagicMock()
        prompt_mock.__or__.return_value = intermediate
        intermediate.__or__.return_value = pipeline_mock
        mock_from_messages.return_value = prompt_mock

        from llms.model import LLMService

        service = object.__new__(LLMService)
        service.prompt_type = "advisor"
        service.streaming = True

        chain = service.build_chain()

        mock_chat_groq.assert_called_once_with(
            groq_api_key="test-key",
            model_name="test-model",
            temperature=0.7,
            streaming=True,
        )
        mock_from_messages.assert_called_once()
        prompt_mock.__or__.assert_called_once_with(mock_llm_instance)
        intermediate.__or__.assert_called_once()
        assert chain is pipeline_mock

    def test_generate_yields_chunks(self):
        """Test that generate yields chunks from the chain."""
        from llms.model import LLMService

        service = object.__new__(LLMService)
        mock_chain = MagicMock()
        mock_chain.stream.return_value = ["chunk1", "chunk2", "chunk3"]
        service.chain = mock_chain

        state = {"user_input": "test input", "messages": []}
        result = list(service.generate(state))

        assert result == ["chunk1", "chunk2", "chunk3"]
        mock_chain.stream.assert_called_once_with({"input": "test input", "messages": [], "ltm_context": ""})

    def test_generate_skips_empty_chunks(self):
        """Test that generate skips empty/falsy chunks."""
        from llms.model import LLMService

        service = object.__new__(LLMService)
        mock_chain = MagicMock()
        mock_chain.stream.return_value = ["chunk1", "", None, "chunk2", False]
        service.chain = mock_chain

        state = {"user_input": "test input", "messages": []}
        result = list(service.generate(state))

        assert result == ["chunk1", "chunk2"]

    def test_generate_handles_exception(self):
        """Test that generate handles exceptions gracefully."""
        from llms.model import LLMService

        service = object.__new__(LLMService)
        mock_chain = MagicMock()
        mock_chain.stream.side_effect = Exception("Test error")
        service.chain = mock_chain

        state = {"user_input": "test input", "messages": []}
        result = list(service.generate(state))

        assert len(result) == 1
        assert "[Error: Model response interrupted.]" in result[0]

    @patch("llms.model.LLMService.build_chain", return_value=MagicMock())
    @patch("llms.model.settings")
    def test_init_with_callbacks(self, mock_settings, mock_build_chain):
        """Test LLMService initialization with custom callbacks."""
        mock_settings.GROQ_API_KEY = "test-key"
        mock_settings.MODEL_NAME = "test-model"
        mock_settings.TEMPERATURE = 0.7

        from llms.model import LLMService

        callbacks = [MagicMock(), MagicMock()]
        service = LLMService(prompt_type="advisor", streaming=True, callbacks=callbacks)

        assert service.callbacks == callbacks

    @patch("llms.model.LLMService.build_chain", return_value=MagicMock())
    @patch("llms.model.settings")
    def test_init_without_callbacks(self, mock_settings, mock_build_chain):
        """Test LLMService initialization without callbacks."""
        mock_settings.GROQ_API_KEY = "test-key"
        mock_settings.MODEL_NAME = "test-model"
        mock_settings.TEMPERATURE = 0.7

        from llms.model import LLMService

        service = LLMService(prompt_type="advisor", streaming=True)

        assert service.callbacks == []
