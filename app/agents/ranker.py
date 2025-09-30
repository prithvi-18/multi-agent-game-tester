import logging
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.models.test_case import TestCase, TestPriority
from app.config import settings

logger = logging.getLogger(__name__)

class RankerAgent:
    """Agent that ranks test cases by priority"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,  # Lower temperature for consistent ranking
            api_key=settings.openai_api_key
        )
    
    async def rank_test_cases(self, test_cases: List[TestCase]) -> List[TestCase]:
        """Rank test cases by importance and feasibility"""
        
        print(f"🎯 RankerAgent: Ranking {len(test_cases)} test cases")
        
        try:
            # Prepare test case summaries
            test_summaries = []
            for test in test_cases:
                summary = f"ID: {test.id} | Name: {test.name} | Type: {test.test_type} | Priority: {test.priority}"
                test_summaries.append(summary)
            
            system_prompt = """You are a test prioritization expert. Rank test cases by importance.
            
            Consider:
            1. Risk coverage (critical functionality)
            2. User impact (how failure affects users)
            3. Automation reliability (easy to automate)
            4. Execution efficiency (time/resources)
            
            Score each test 0-100 (higher = more important)."""
            
            human_prompt = f"""Rank these test cases by importance (0-100 score):
            
{chr(10).join(test_summaries)}

Return format:
test_001: 95
test_002: 87
test_003: 76
..."""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            
            # Parse rankings and apply to test cases
            self._apply_rankings(test_cases, response.content)
            
            # Sort by rank score (highest first)
            ranked_tests = sorted(test_cases, key=lambda t: t.rank_score or 0, reverse=True)
            
            print(f"✅ Ranked {len(ranked_tests)} test cases")
            return ranked_tests
            
        except Exception as e:
            print(f"❌ Error ranking test cases: {e}")
            return self._fallback_ranking(test_cases)
    
    def _apply_rankings(self, test_cases: List[TestCase], response: str):
        """Apply AI rankings to test cases"""
        
        lines = response.strip().split('\n')
        
        for line in lines:
            if ':' in line:
                try:
                    test_id, score_str = line.split(':', 1)
                    test_id = test_id.strip()
                    score = float(score_str.strip())
                    
                    # Find test case and apply score
                    for test in test_cases:
                        if test.id == test_id:
                            test.rank_score = score
                            break
                            
                except Exception as e:
                    print(f"⚠️ Couldn't parse ranking line: {line}")
                    continue
    
    def _fallback_ranking(self, test_cases: List[TestCase]) -> List[TestCase]:
        """Fallback ranking based on priority"""
        
        print("📊 Using fallback ranking based on priority")
        
        for test in test_cases:
            # Simple priority-based scoring
            if test.priority == TestPriority.HIGH:
                test.rank_score = 90.0
            elif test.priority == TestPriority.MEDIUM:
                test.rank_score = 70.0
            else:
                test.rank_score = 50.0
        
        return sorted(test_cases, key=lambda t: t.rank_score or 0, reverse=True)
