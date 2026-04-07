"""
ProjectSmith AI root entrypoint.

This module provides a lightweight compatibility layer for running
the application from the repository root and for CI tests.
"""

from llms.model import LLMService


def main():
    """Run a minimal persona-based loop using LLMService."""
    prompt_type = input("Select persona: ").strip()
    service = LLMService(prompt_type=prompt_type)

    while True:
        user_input = input().strip()
        if user_input.lower() in ("exit", "quit"):
            break

        # Consume the generator output so the loop executes fully.
        list(service.generate(user_input))


if __name__ == "__main__":
    main()
