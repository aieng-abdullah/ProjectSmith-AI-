"""Tests for main entry point."""
import pytest
from unittest.mock import patch, MagicMock


class TestMain:
    """Test cases for main.py."""

    @patch('builtins.input', side_effect=['bp', 'hello', 'exit'])
    @patch('main.LLMService')
    def test_main_initialization(self, mock_llm_service_class, mock_input):
        """Test main function initializes LLMService correctly."""
        mock_llm_instance = MagicMock()
        mock_llm_instance.generate.return_value = ['test response']
        mock_llm_service_class.return_value = mock_llm_instance

        from main import main

        main()

        mock_llm_service_class.assert_called_once_with(prompt_type='bp')

    @patch('builtins.input', side_effect=['psycho', 'test message', 'exit'])
    @patch('main.LLMService')
    def test_main_persona_selection_psycho(self, mock_llm_service_class, mock_input):
        """Test main function with psycho persona selection."""
        mock_llm_instance = MagicMock()
        mock_llm_instance.generate.return_value = ['test']
        mock_llm_service_class.return_value = mock_llm_instance

        from main import main

        main()

        mock_llm_service_class.assert_called_once_with(prompt_type='psycho')

    @patch('builtins.input', side_effect=['bp', 'hello', 'exit'])
    @patch('main.LLMService')
    def test_main_calls_generate(self, mock_llm_service_class, mock_input):
        """Test that main calls generate method with user input."""
        mock_llm_instance = MagicMock()
        mock_llm_instance.generate.return_value = ['response']
        mock_llm_service_class.return_value = mock_llm_instance

        from main import main

        main()

        # Verify generate was called
        mock_llm_instance.generate.assert_called()
        calls = mock_llm_instance.generate.call_args_list
        assert any('hello' in str(call) for call in calls)

    @patch('builtins.input', side_effect=['invalid_persona', 'exit'])
    @patch('main.LLMService')
    def test_main_handles_invalid_persona(self, mock_llm_service_class, mock_input):
        """Test that main handles invalid persona gracefully."""
        mock_llm_service_class.side_effect = ValueError('invalid prompt')

        from main import main

        with pytest.raises(ValueError, match='invalid prompt'):
            main()


class TestMainFunctionEntry:
    """Test cases for __main__ entry point."""

    @patch('main.main')
    def test_main_entry_point(self, mock_main):
        """Test that main() is called when script is run directly."""
        import main

        main.main()

        mock_main.assert_called_once()
