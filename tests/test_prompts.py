"""Tests for prompt templates."""


class TestPrompts:
    """Test cases for prompt strings."""

    def test_advisor_prompt_exists(self):
        """Test that advisor_prompt is defined and non-empty."""
        from llms.prompts import advisor_prompt

        assert advisor_prompt is not None
        assert isinstance(advisor_prompt, str)
        assert len(advisor_prompt) > 0
        assert "startup advisor" in advisor_prompt.lower()

    def test_chat_prompt_exists(self):
        """Test that chat_prompt is defined and non-empty."""
        from llms.prompts import chat_prompt

        assert chat_prompt is not None
        assert isinstance(chat_prompt, str)
        assert len(chat_prompt) > 0
        assert "projectsmith" in chat_prompt.lower()

    def test_planner_prompt_exists(self):
        """Test that planner_prompt is defined and non-empty."""
        from llms.prompts import planner_prompt

        assert planner_prompt is not None
        assert isinstance(planner_prompt, str)
        assert len(planner_prompt) > 0
        assert "phase 1 — build this first" in planner_prompt.lower()

    def test_cost_prompt_exists(self):
        """Test that cost_prompt is defined and non-empty."""
        from llms.prompts import cost_prompt

        assert cost_prompt is not None
        assert isinstance(cost_prompt, str)
        assert len(cost_prompt) > 0
        assert "free to start" in cost_prompt.lower()

    def test_edge_case_prompt_exists(self):
        """Test that edge_case_prompt is defined and non-empty."""
        from llms.prompts import edge_case_prompt

        assert edge_case_prompt is not None
        assert isinstance(edge_case_prompt, str)
        assert len(edge_case_prompt) > 0
        assert "risk 1 —" in edge_case_prompt.lower()

    def test_doc_prompt_exists(self):
        """Test that doc_prompt is defined and non-empty."""
        from llms.prompts import doc_prompt

        assert doc_prompt is not None
        assert isinstance(doc_prompt, str)
        assert len(doc_prompt) > 0
        assert "what you're building:" in doc_prompt.lower()

    def test_prompts_are_different(self):
        """Test that all prompts are different from each other."""
        from llms.prompts import (
            advisor_prompt,
            chat_prompt,
            planner_prompt,
            cost_prompt,
            edge_case_prompt,
            doc_prompt,
        )

        assert len({advisor_prompt, chat_prompt, planner_prompt, cost_prompt, edge_case_prompt, doc_prompt}) == 6
