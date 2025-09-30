import asyncio, logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from app.models.test_case import TestCase

logger = logging.getLogger(__name__)

class BrowserService:
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.contexts: Dict[str, BrowserContext] = {}

    async def initialize(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        logger.info("✅ Playwright browser initialized")

    async def cleanup(self):
        for ctx in self.contexts.values():
            await ctx.close()
        self.contexts.clear()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("🗑️ Browser service cleaned up")

    async def execute_test_case(self, test_case: TestCase, target_url: str, task_id: str) -> Dict[str, Any]:
        start = datetime.now()
        ctx = await self.browser.new_context()
        page = await ctx.new_page()
        artifacts: List[str] = []

        try:
            # Navigate to game
            await page.goto(target_url, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)  # Let game load
            
            # Handle language selection (if present)
            try:
                english_btn = page.locator('text="English"')
                if await english_btn.is_visible(timeout=3000):
                    await english_btn.click()
                    await page.wait_for_timeout(1000)
            except:
                pass  # Language selection might not be present
            
            artifacts.append(await self._capture_screenshot(task_id, test_case.id, page, "start"))

            # Execute test steps with game-specific logic
            for i, step in enumerate(test_case.steps):
                await self._execute_game_step(page, step, i)
                artifacts.append(await self._capture_screenshot(task_id, test_case.id, page, f"step_{i+1}"))

            verdict = "PASS"
            
        except Exception as e:
            verdict = "FAIL"
            logger.error(f"Test {test_case.id} failed: {e}")
            artifacts.append(await self._capture_screenshot(task_id, test_case.id, page, "error"))
        finally:
            await page.close()
            await ctx.close()

        duration = int((datetime.now() - start).total_seconds() * 1000)
        return {
            "test_case_id": test_case.id,
            "start_time": start.isoformat(),
            "duration_ms": duration,
            "status": verdict,
            "verdict": verdict,
            "artifacts": artifacts,
        }

    async def _execute_game_step(self, page: Page, step: str, step_num: int):
        """Execute game-specific test steps"""
        step_lower = step.lower()
        
        if "navigate" in step_lower:
            # Already handled in main execute function
            pass
        elif "click" in step_lower:
            if "hint" in step_lower or "💡" in step_lower:
                # Try to find hint button
                await page.click('button:has-text("💡"), button:has-text("hint"), [title*="hint"]', timeout=5000)
            elif "new game" in step_lower:
                await page.click('button:has-text("New Game"), button:has-text("Continue")', timeout=5000)  
            elif "number" in step_lower:
                # Click on number tiles (game-specific)
                await page.click('.number, .tile, .cell', timeout=5000)
            else:
                # Generic button click
                await page.click('button', timeout=5000)
        elif "wait" in step_lower or "load" in step_lower:
            if "page" in step_lower:
                await page.wait_for_load_state("domcontentloaded")
            else:
                await page.wait_for_timeout(2000)
        elif "verify" in step_lower or "check" in step_lower:
            if "score" in step_lower:
                # Wait for score element to be visible
                await page.wait_for_selector('[class*="score"], #score, .points', timeout=5000)
            elif "board" in step_lower or "game" in step_lower:
                await page.wait_for_selector('.game-board, .grid, canvas', timeout=5000)

    async def _capture_screenshot(self, task_id: str, test_id: str, page: Page, label: str) -> str:
        path = Path(f"artifacts/screenshots/{task_id}_{test_id}_{label}.png")
        path.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(path), full_page=True)
        return str(path)
