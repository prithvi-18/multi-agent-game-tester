import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime

from app.models.test_case import TestCase
from app.services.browser_service import BrowserService

logger = logging.getLogger(__name__)

class ExecutorAgent:
    """Agent responsible for executing test cases with real browser automation"""

    def __init__(self):
        # Initialize the browser service
        self.browser_service = BrowserService()
        self.max_concurrent_tests = 3  # Limit concurrent browser contexts

    async def initialize(self):
        """Initialize browser service"""
        await self.browser_service.initialize()

    async def cleanup(self):
        """Cleanup browser service"""
        await self.browser_service.cleanup()

    async def execute_test_cases(
        self,
        test_cases: List[TestCase],
        target_url: str,
        task_id: str,
        timeout_seconds: int = 300
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple test cases in parallel using Playwright.
        Initializes browser service, runs tests, then cleans up.
        """
        logger.info(f"ExecutorAgent: Executing {len(test_cases)} test cases")

        # Ensure browser service is ready
        await self.initialize()

        semaphore = asyncio.Semaphore(self.max_concurrent_tests)

        async def run_single(test_case: TestCase) -> Dict[str, Any]:
            async with semaphore:
                return await self.browser_service.execute_test_case(
                    test_case=test_case,
                    target_url=target_url,
                    task_id=task_id
                )

        # Launch all tasks
        tasks = [run_single(tc) for tc in test_cases]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed: List[Dict[str, Any]] = []
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                logger.error(f"Error executing {test_cases[i].id}: {res}")
                processed.append({
                    "test_case_id": test_cases[i].id,
                    "start_time": datetime.now().isoformat(),
                    "duration_ms": 0,
                    "status": "ERROR",
                    "verdict": "FAIL",
                    "artifacts": [],
                    "error_message": str(res)
                })
            else:
                processed.append(res)

        # Clean up browser contexts
        await self.cleanup()

        logger.info(f"ExecutorAgent: Completed execution of {len(processed)} test cases")
        return processed
