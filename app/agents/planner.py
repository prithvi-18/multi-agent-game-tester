import asyncio
import logging
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.models.test_case import TestCase, TestCaseType, TestPriority
from app.config import settings

logger = logging.getLogger(__name__)

class PlannerAgent:
    """Agent that generates test cases for the game"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=settings.openai_api_key
        )
    
    async def generate_test_cases(self, target_url: str, count: int = 20) -> List[TestCase]:
        """Generate test cases for the target game"""
        
        print(f"🤖 PlannerAgent: Generating {count} test cases for {target_url}")
        
        system_prompt = """You are an expert game testing agent. Generate comprehensive test cases for web games.
        
        Focus on:
        1. UI interactions (clicks, navigation)
        2. Game mechanics (rules, scoring)
        3. Performance (loading, responsiveness)
        4. Error handling (invalid inputs, edge cases)
        
        Each test should be clear and actionable."""
        
        human_prompt = f"""Generate {count} test cases for this puzzle game: {target_url}
        
        This is SumLink - a number matching puzzle game with:
        - Grid-based number placement
        - Score tracking
        - Hint system
        - Multi-language support
        
        Return test cases in this format for each:
        Name: [Test name]
        Description: [What it tests]
        Type: [UI_INTERACTION/GAME_MECHANICS/PERFORMANCE/ERROR_HANDLING]
        Priority: [HIGH/MEDIUM/LOW]
        Steps: [Step 1, Step 2, Step 3...]
        Expected: [Expected outcome]
        Validation: [How to verify success]
        ---"""
        
        try:
            # Get AI response
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            test_cases = self._parse_response_to_test_cases(response.content)
            
            print(f"✅ Generated {len(test_cases)} test cases")
            return test_cases
            
        except Exception as e:
            print(f"❌ Error generating test cases: {e}")
            return self._get_fallback_test_cases(count)
    
    def _parse_response_to_test_cases(self, response: str) -> List[TestCase]:
        """Parse AI response into TestCase objects"""
        test_cases = []
        
        # Split response by test case separator
        test_blocks = response.split('---')
        
        for i, block in enumerate(test_blocks[:20]):  # Limit to 20 tests
            if not block.strip():
                continue
                
            try:
                # Extract information from each block
                lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
                
                # Parse fields (simplified parsing)
                name = "Test Case"
                description = "Generated test case"
                test_type = TestCaseType.UI_INTERACTION
                priority = TestPriority.MEDIUM
                steps = ["Navigate to game", "Perform test action", "Verify result"]
                expected = "Test passes successfully"
                validation = ["Check result matches expected outcome"]
                
                # Try to extract actual values
                for line in lines:
                    if line.startswith('Name:'):
                        name = line.replace('Name:', '').strip()
                    elif line.startswith('Description:'):
                        description = line.replace('Description:', '').strip()
                    elif line.startswith('Type:'):
                        type_str = line.replace('Type:', '').strip()
                        if type_str in ['UI_INTERACTION', 'GAME_MECHANICS', 'PERFORMANCE', 'ERROR_HANDLING']:
                            test_type = TestCaseType(type_str)
                    elif line.startswith('Priority:'):
                        priority_str = line.replace('Priority:', '').strip()
                        if priority_str in ['HIGH', 'MEDIUM', 'LOW']:
                            priority = TestPriority(priority_str)
                    elif line.startswith('Steps:'):
                        steps_str = line.replace('Steps:', '').strip()
                        steps = [s.strip() for s in steps_str.split(',')]
                    elif line.startswith('Expected:'):
                        expected = line.replace('Expected:', '').strip()
                    elif line.startswith('Validation:'):
                        validation_str = line.replace('Validation:', '').strip()
                        validation = [validation_str]
                
                test_case = TestCase(
                    id=f"test_{i+1:03d}",
                    name=name,
                    description=description,
                    test_type=test_type,
                    priority=priority,
                    steps=steps,
                    expected_outcome=expected,
                    validation_criteria=validation
                )
                
                test_cases.append(test_case)
                
            except Exception as e:
                print(f"⚠️ Couldn't parse test case {i+1}: {e}")
                continue
        
        return test_cases

    def _get_fallback_test_cases(self, count: int) -> List[TestCase]:
        """SumLink game-specific fallback test cases"""
        sumlink_tests = [
            TestCase(
                id="test_001",
                name="Language Selection Test",
                description="Test the language selection screen that appears first",
                test_type=TestCaseType.UI_INTERACTION,
                priority=TestPriority.HIGH,
                steps=[
                    "Navigate to SumLink game URL",
                    "Wait for language selection screen",
                    "Click on English button",
                    "Wait for game to load",
                    "Verify game board appears"
                ],
                expected_outcome="Successfully selects English and loads game",
                validation_criteria=["Language screen appears", "English selection works", "Game loads"]
            ),
            TestCase(
                id="test_002",
                name="Game Board Load Test",
                description="Verify the main game board loads properly",
                test_type=TestCaseType.UI_INTERACTION,
                priority=TestPriority.HIGH,
                steps=[
                    "Navigate to game",
                    "Select English language",
                    "Wait for game board to appear",
                    "Check for game elements",
                    "Verify no loading errors"
                ],
                expected_outcome="Game board loads successfully with all elements",
                validation_criteria=["Game board visible", "No error messages", "Interactive elements present"]
            ),
            TestCase(
                id="test_003",
                name="Basic Game Interaction Test",
                description="Test basic clicking and interaction with game",
                test_type=TestCaseType.GAME_MECHANICS,
                priority=TestPriority.MEDIUM,
                steps=[
                    "Load game and select English",
                    "Click on game elements",
                    "Try to interact with numbers/tiles",
                    "Check for visual feedback",
                    "Verify game responds to clicks"
                ],
                expected_outcome="Game responds to user interactions",
                validation_criteria=["Clicks register", "Visual feedback works", "Game is interactive"]
            )
        ]

        # Return the requested number of tests (repeat if needed)
        result: List[TestCase] = []
        for i in range(count):
            base = sumlink_tests[i % len(sumlink_tests)]
            result.append(TestCase(
                id=f"sumlink_{i+1:03d}",
                name=f"{base.name} #{i+1}",
                description=base.description,
                test_type=base.test_type,
                priority=base.priority,
                steps=base.steps,
                expected_outcome=base.expected_outcome,
                validation_criteria=base.validation_criteria
            ))

        return result[:count]

