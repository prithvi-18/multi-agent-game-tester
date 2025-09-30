from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class TestCaseType(str, Enum):
    UI_INTERACTION = "UI_INTERACTION"
    GAME_MECHANICS = "GAME_MECHANICS"
    PERFORMANCE = "PERFORMANCE"
    ERROR_HANDLING = "ERROR_HANDLING"

class TestPriority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class TestCase(BaseModel):
    id: str
    name: str
    description: str
    test_type: TestCaseType
    priority: TestPriority
    steps: List[str]
    expected_outcome: str
    validation_criteria: List[str]
    estimated_duration: int = 60  # seconds
    rank_score: Optional[float] = None

class TestReport(BaseModel):
    task_id: str
    target_url: str
    timestamp: datetime
    total_candidates: int
    executed_tests: int
    success_rate: float
    execution_results: List[Dict[str, Any]] = []
    artifacts: List[str] = []

from datetime import datetime
from typing import List, Dict, Any, Optional

class DetailedTestReport(BaseModel):
    """Enhanced test report with more metrics"""
    task_id: str
    target_url: str
    timestamp: datetime
    
    # Test summary
    total_candidates: int
    executed_tests: int
    passed_tests: int
    failed_tests: int
    success_rate: float
    
    # Execution details
    total_duration_ms: int
    average_test_duration_ms: float
    fastest_test_ms: int
    slowest_test_ms: int
    
    # Game-specific metrics
    language_selection_success: bool = False
    game_loading_time_ms: Optional[int] = None
    ui_interactions_successful: int = 0
    
    # Results and artifacts
    execution_results: List[Dict[str, Any]] = []
    artifacts: List[str] = []
    screenshots_captured: int = 0
    
    # Analysis
    most_common_failure: Optional[str] = None
    reliability_score: float = 0.0  # 0-1 based on consistency
