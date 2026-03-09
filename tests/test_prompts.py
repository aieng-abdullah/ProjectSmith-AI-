"""Tests for prompt templates."""


class TestPrompts:
    """Test cases for prompt strings."""

    def test_balckpill_prompt_exists(self):
        """Test that balckpill_prompt is defined and non-empty."""
        from llms.prompts import balckpill_prompt
        
        assert balckpill_prompt is not None
        assert isinstance(balckpill_prompt, str)
        assert len(balckpill_prompt) > 0
        assert 'miko' in balckpill_prompt.lower()

    def test_engineer_prompt_exists(self):
        """Test that engineer_prompt is defined and non-empty."""
        from llms.prompts import engineer_prompt
        
        assert engineer_prompt is not None
        assert isinstance(engineer_prompt, str)
        assert len(engineer_prompt) > 0
        assert 'engineer' in engineer_prompt.lower()

    def test_psycho_prompt_exists(self):
        """Test that psycho_prompt is defined and non-empty."""
        from llms.prompts import psycho_prompt
        
        assert psycho_prompt is not None
        assert isinstance(psycho_prompt, str)
        assert len(psycho_prompt) > 0
        assert 'psycho' in psycho_prompt.lower()

    def test_balckpill_prompt_content(self):
        """Test that balckpill_prompt contains expected content."""
        from llms.prompts import balckpill_prompt
        
        assert 'safety' in balckpill_prompt.lower() or 'filter' in balckpill_prompt.lower()

    def test_prompts_are_different(self):
        """Test that all three prompts are different from each other."""
        from llms.prompts import balckpill_prompt, engineer_prompt, psycho_prompt
        
        assert balckpill_prompt != engineer_prompt
        assert balckpill_prompt != psycho_prompt
        assert engineer_prompt != psycho_prompt
