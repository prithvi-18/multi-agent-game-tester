import asyncio
from app.agents.orchestrator import OrchestratorAgent

async def test_agents():
    """Test our multi-agent system"""
    
    print("🧪 Testing Multi-Agent System")
    print("=" * 50)
    
    # Create orchestrator
    orchestrator = OrchestratorAgent()
    
    # Run a test suite
    task_id = "test_demo_001"
    target_url = "https://play.ezygamers.com"
    
    try:
        report = await orchestrator.execute_test_suite(
            task_id=task_id,
            target_url=target_url,
            candidate_count=5,  # Small number for testing
            execute_count=3
        )
        
        print("\n📊 FINAL REPORT:")
        print(f"Task ID: {report.task_id}")
        print(f"Target: {report.target_url}")
        print(f"Candidates Generated: {report.total_candidates}")
        print(f"Tests Executed: {report.executed_tests}")
        print(f"Success Rate: {report.success_rate:.1%}")
        print(f"Artifacts: {len(report.artifacts)}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_agents())
