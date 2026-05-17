# agents/sub_agents/base.py
import logging
from typing import Optional
from agents.supervisor_state import SubAgentResult

logger = logging.getLogger(__name__)


class BaseSubAgent:
    name: str

    def run(self, idea: str, context: str) -> SubAgentResult:
        raise NotImplementedError

    def _safe_run(self, idea: str, context: str) -> SubAgentResult:
        try:
            logger.info(f"[{self.name}] start | idea={idea[:50]}...")
            result = self.run(idea, context)
            logger.info(f"[{self.name}] done | success={result['success']}")
            return result
        except Exception as e:
            logger.error(f"[{self.name}] failed | error={str(e)}")
            return SubAgentResult(
                agent_name=self.name,
                output="",
                success=False,
                error=str(e)
            )
