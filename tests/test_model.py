"""Tests for LLM model service."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from langchain_core.prompts import ChatPromptTemplate


class TestLLMService:
    """Test cases for LLMService class."""

    @patch('llms.model.settings')
    @patch('llms.model.ChatGroq')
    def test_init_with_valid_prompt_type(self, mock_chat_groq, mock_settings):
        """Test LLMService initialization with valid prompt type."""
        mock_settings.GROQ_API_KEY = 'test-key'
        mock_settings.MODEL_NAME = 'test-model'
        mock_settings.TEMPERATURE = 0.7
        
        from llms.model import LLMService
        
        service = LLMService(prompt_type='bp', streaming=True)
        
        assert service.prompt_type == 'bp'
        assert service.streaming is True
        assert service.chain is not None

    @patch('llms.model.settings')
    def test_get_prompt_bp(self, mock_settings):
        """Test getting blackpill prompt."""
        mock_settings.GROQ_API_KEY = 'test-key'
        mock_settings.MODEL_NAME = 'test-model'
        mock_settings.TEMPERATURE = 0.7
        
        from llms.model import LLMService
        
        service = LLMService(prompt_type='bp', streaming=False)
        prompt = service.get_prompt('bp')
        
        assert isinstance(prompt, ChatPromptTemplate)

    @patch('llms.model.settings')
    def test_get_prompt_psycho(self, mock_settings):
        """Test getting psycho prompt."""
        mock_settings.GROQ_API_KEY = 'test-key'
        mock_settings.MODEL_NAME = 'test-model'
        mock_settings.TEMPERATURE = 0.7
        
        from llms.model import LLMService
        
        service = LLMService(prompt_type='psycho', streaming=False)
        prompt = service.get_prompt('psycho')
        
        assert isinstance(prompt, ChatPromptTemplate)

    @patch('llms.model.settings')
    def test_get_prompt_engineer(self, mock_settings):
        """Test getting engineer prompt (note: typo in code 'eninner')."""
        mock_settings.GROQ_API_KEY = 'test-key'
        mock_settings.MODEL_NAME = 'test-model'
        mock_settings.TEMPERATURE = 0.7
        
        from llms.model import LLMService
        
        service = LLMService(prompt_type='eninner', streaming=False)
        prompt = service.get_prompt('eninner')
        
        assert isinstance(prompt, ChatPromptTemplate)

    @patch('llms.model.settings')
    def test_get_prompt_invalid(self, mock_settings):
        """Test that invalid prompt type raises ValueError."""
        mock_settings.GROQ_API_KEY = 'test-key'
        mock_settings.MODEL_NAME = 'test-model'
        mock_settings.TEMPERATURE = 0.7
        
        from llms.model import LLMService
        
        service = LLMService(prompt_type='bp', streaming=False)
        
        with pytest.raises(ValueError, match="invalid prompt"):
            service.get_prompt('invalid')

    @patch('llms.model.settings')
    @patch('llms.model.ChatGroq')
    def test_build_chain_creates_pipeline(self, mock_chat_groq, mock_settings):
        """Test that build_chain creates a proper pipeline."""
        mock_settings.GROQ_API_KEY = 'test-key'
        mock_settings.MODEL_NAME = 'test-model'
        mock_settings.TEMPERATURE = 0.7
        
        mock_llm_instance = MagicMock()
        mock_chat_groq.return_value = mock_llm_instance
        
        from llms.model import LLMService
        
        service = LLMService(prompt_type='bp', streaming=True)
        chain = service.build_chain()
        
        # Verify ChatGroq was called with correct parameters
        mock_chat_groq.assert_called_once_with(
            groq_api_key='test-key',
            model_name='test-model',
            temperature=0.7,
            streaming=True
        )
        assert chain is not None

    @patch('llms.model.settings')
    def test_generate_yields_chunks(self, mock_settings):
        """Test that generate yields chunks from the chain."""
        mock_settings.GROQ_API_KEY = 'test-key'
        mock_settings.MODEL_NAME = 'test-model'
        mock_settings.TEMPERATURE = 0.7
        
        from llms.model import LLMService
        
        service = LLMService(prompt_type='bp', streaming=False)
        
        # Mock the chain
        mock_chain = MagicMock()
        mock_chain.stream.return_value = ['chunk1', 'chunk2', 'chunk3']
        service.chain = mock_chain
        
        result = list(service.generate('test input'))
        
        assert result == ['chunk1', 'chunk2', 'chunk3']
        mock_chain.stream.assert_called_once_with({'input': 'test input'})

    @patch('llms.model.settings')
    def test_generate_skips_empty_chunks(self, mock_settings):
        """Test that generate skips empty/falsy chunks."""
        mock_settings.GROQ_API_KEY = 'test-key'
        mock_settings.MODEL_NAME = 'test-model'
        mock_settings.TEMPERATURE = 0.7
        
        from llms.model import LLMService
        
        service = LLMService(prompt_type='bp', streaming=False)
        
        # Mock the chain with empty chunks
        mock_chain = MagicMock()
        mock_chain.stream.return_value = ['chunk1', '', None, 'chunk2', False]
        service.chain = mock_chain
        
        result = list(service.generate('test input'))
        
        assert result == ['chunk1', 'chunk2']

    @patch('llms.model.settings')
    def test_generate_handles_exception(self, mock_settings):
        """Test that generate handles exceptions gracefully."""
        mock_settings.GROQ_API_KEY = 'test-key'
        mock_settings.MODEL_NAME = 'test-model'
        mock_settings.TEMPERATURE = 0.7
        
        from llms.model import LLMService
        
        service = LLMService(prompt_type='bp', streaming=False)
        
        # Mock the chain to raise exception
        mock_chain = MagicMock()
        mock_chain.stream.side_effect = Exception('Test error')
        service.chain = mock_chain
        
        result = list(service.generate('test input'))
        
        assert len(result) == 1
        assert '[Error: Model response interrupted.]' in result[0]

    @patch('llms.model.settings')
    def test_init_with_callbacks(self, mock_settings):
        """Test LLMService initialization with custom callbacks."""
        mock_settings.GROQ_API_KEY = 'test-key'
        mock_settings.MODEL_NAME = 'test-model'
        mock_settings.TEMPERATURE = 0.7
        
        from llms.model import LLMService
        
        callbacks = [MagicMock(), MagicMock()]
        service = LLMService(prompt_type='bp', streaming=True, callbacks=callbacks)
        
        assert service.callbacks == callbacks

    @patch('llms.model.settings')
    def test_init_without_callbacks(self, mock_settings):
        """Test LLMService initialization without callbacks."""
        mock_settings.GROQ_API_KEY = 'test-key'
        mock_settings.MODEL_NAME = 'test-model'
        mock_settings.TEMPERATURE = 0.7
        
        from llms.model import LLMService
        
        service = LLMService(prompt_type='bp', streaming=True)
        
        assert service.callbacks == []
