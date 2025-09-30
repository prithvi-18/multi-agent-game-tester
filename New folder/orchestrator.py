import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from app.agents.planner import PlannerAgent
from app.agents.ranker import RankerAgent
from app.agents.executor import ExecutorAgent
from app.models.test_case import TestCase, TestReport

logger = logging.getLogger(__name__)

class OrchestratorAgent:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self):
        # Initialize all agents
        self.planner = PlannerAgent()
        self.ranker = RankerAgent()
        self.executor = ExecutorAgent()
        
        # Task tracking
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
    
    async def execute_test_suite(self, task_id: str, target_url: str, 
                               candidate_count: int = 20, execute_count: int = 10) -> TestReport:
        """Execute the complete multi-agent test workflow"""
        
        print(f"🎯 OrchestratorAgent: Starting test suite {task_id}")
        
        # Update task status
        self._update_task_status(task_id, "planning", "Generating test case candidates")
        
        try:
            # Phase 1: Generate test cases
            print("\n📋 Phase 1: Generating test cases...")
            candidate_tests = await self.planner.generate_test_cases(target_url, candidate_count)
            
            # Phase 2: Rank test cases  
            print("\n📊 Phase 2: Ranking test cases...")
            self._update_task_status(task_id, "ranking", "Ranking test cases by priority")
            ranked_tests = await self.ranker.rank_test_cases(candidate_tests)
            
            # Phase 3: Select top tests for execution
            selected_tests = ranked_tests[:execute_count]
            print(f"\n🎯 Selected top {len(selected_tests)} tests for execution")
            
            # Phase 4: Execute tests
            print("\n🚀 Phase 3: Executing test cases...")
            self._update_task_status(task_id, "executing", f"Executing top {execute_count} test cases")
            execution_results = await self.executor.execute_test_cases(selected_tests, target_url, task_id)
            
            # Phase 5: Generate report
            print("\n📊 Phase 4: Generating report...")
            self._update_task_status(task_id, "reporting", "Generating comprehensive test report")
            
            # Calculate success rate
            successful_tests = sum(1 for result in execution_results if result.get("verdict") == "PASS")
            success_rate = successful_tests / len(execution_results) if execution_results else 0
            
            # Create comprehensive report
            test_report = TestReport(
                task_id=task_id,
                target_url=target_url,
                timestamp=datetime.now(timezone.utc),
                total_candidates=len(candidate_tests),
                executed_tests=len(execution_results),
                success_rate=success_rate,
                execution_results=execution_results,
                artifacts=self._collect_artifacts(execution_results)
            )
            
            # Mark as completed
            self._update_task_status(task_id, "completed", "Test execution completed successfully")
            
            print(f"\n✅ Test suite {task_id} completed!")
            print(f"   📊 Success Rate: {success_rate:.1%}")
            print(f"   📁 Artifacts: {len(test_report.artifacts)} files")
            
            return test_report
            
        except Exception as e:
            print(f"\n❌ Test suite {task_id} failed: {e}")
            self._update_task_status(task_id, "failed", str(e))
            raise
    
    def _update_task_status(self, task_id: str, status: str, message: str):
        """Update task status"""
        self.active_tasks[task_id] = {
            "status": status,
            "message": message,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        print(f"📌 Status: {status} - {message}")
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get current task status"""
        return self.active_tasks.get(task_id)
    
    def _collect_artifacts(self, execution_results: List[Dict[str, Any]]) -> List[str]:
        """Collect all artifacts from execution results"""
        artifacts = []
        for result in execution_results:
            artifacts.extend(result.get("artifacts", []))
        return artifacts
