#!/usr/bin/env python
"""Pre-deploy health check script."""

import os
import sys
from pathlib import Path

# Add src to path
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)


def step(msg: str):
    print(f"\n✓ {msg}")


def fail(msg: str):
    print(f"\n✗ {msg}")
    sys.exit(1)


def main():
    print("━" * 70)
    print("ProjectSmith AI — Pre-Deployment Checklist")
    print("━" * 70)

    # Step 1: Tests pass
    print("\n[1/5] Running unit tests...")
    os.system("$env:PYTHONPATH='src'; python -m pytest tests/unit/ -q --tb=short")
    if (
        os.system("$env:PYTHONPATH='src'; python -m pytest tests/unit/ -q --tb=short")
        != 0
    ):
        fail("Unit tests failed")
    step("Unit tests passed")

    # Step 2: Graph compiles
    print("\n[2/5] Verifying supervisor graph compiles...")
    try:
        from agents.supervisor.supervisor import supervisor

        step("Supervisor graph compiled successfully")
    except Exception as e:
        fail(f"Graph compilation failed: {e}")

    # Step 3: Env vars validated
    print("\n[3/5] Checking environment variables...")
    from llms.config import settings

    required = [
        "GROQ_API_KEY",
        "POSTGRES_URL",
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "MODEL_NAME",
    ]
    missing = [v for v in required if not getattr(settings, v, None)]
    if missing:
        fail(f"Missing env vars: {missing}")
    step("All required environment variables present")

    # Step 4: Smoke test (local only)
    print("\n[4/5] Smoke test (supervisor invocation)...")
    try:
        from langchain_core.messages import HumanMessage

        result = supervisor.invoke(
            {
                "messages": [HumanMessage(content="test")],
                "idea": "test",
                "context": "test",
            },
            config={"configurable": {"thread_id": "smoke"}},
        )
        if "intent" in result:
            step("Smoke test passed")
        else:
            fail("Smoke test returned unexpected shape")
    except Exception as e:
        fail(f"Smoke test failed: {e}")

    # Summary
    print("\n" + "=" * 70)
    print("✓ All 4 checks passed — ready to deploy!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. docker-compose up -d")
    print("  2. curl -f http://localhost:8000/")
    print("  3. git push origin main")
    print("=" * 70)


if __name__ == "__main__":
    main()
