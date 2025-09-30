import asyncio
from app.agents.orchestrator import OrchestratorAgent

async def demo_execution():
    """Demo script for video recording"""
    print("🎬 DEMO: Multi-Agent Game Tester")
    print("=" * 50)
    
    orchestrator = OrchestratorAgent()
    
    # Demo with smaller numbers for quick video
    task_id = "demo_video_001"
    target_url = "https://play.ezygamers.com"
    
    print(f"🎯 Target Game: SumLink Puzzle")
    print(f"📋 Generating 8 test candidates")
    print(f"🚀 Executing top 4 tests")
    print(f"📊 Capturing artifacts and generating report")
    print()
    
    try:
        report = await orchestrator.execute_test_suite(
            task_id=task_id,
            target_url=target_url,
            candidate_count=8,
            execute_count=4
        )
        
        print("\n🎉 DEMO COMPLETED!")
        print(f"✅ Success Rate: {report.success_rate:.1%}")
        print(f"📸 Screenshots: Check artifacts/screenshots/")
        print(f"📄 Full Report: Available via API")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    asyncio.run(demo_execution())
