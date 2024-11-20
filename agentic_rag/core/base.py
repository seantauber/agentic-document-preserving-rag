"""
Foundation for all system agents.
"""
from dataclasses import dataclass, field
from typing import Set, Any, List, Dict, Optional
from datetime import datetime
import asyncio

@dataclass
class AgentState:
    """Represents the current state of an agent"""
    active: bool = False
    current_task: Optional[Any] = None
    memory: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Task:
    """Represents a task to be executed by an agent"""
    id: str
    type: str
    data: Any
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Plan:
    """Represents a planned sequence of actions"""
    tasks: List[Task]
    dependencies: Dict[str, List[str]]
    estimated_duration: float
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Result:
    """Represents the result of a task execution"""
    task_id: str
    status: str
    data: Any
    error: Optional[Exception] = None
    completion_time: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)  # Added metadata field

@dataclass
class Experience:
    """Represents an agent's experience from task execution"""
    task: Task
    result: Result
    duration: float
    context: Dict[str, Any]

@dataclass
class AgentMessage:
    """Represents a message between agents"""
    sender: str
    recipient: str
    content: Any
    type: str
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: str = field(default_factory=lambda: str(datetime.now().timestamp()))

@dataclass
class Response:
    """Represents a response to a message or task"""
    status: str
    data: Any
    metadata: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)

class KnowledgeBase:
    """Manages agent's knowledge and learning"""
    def __init__(self):
        self.facts: Dict[str, Any] = {}
        self.rules: Dict[str, Any] = {}
        self.experiences: List[Experience] = []

    def add_experience(self, exp: Experience) -> None:
        """Add a new experience to learn from"""
        self.experiences.append(exp)
        self._update_knowledge(exp)

    def query(self, context: Dict[str, Any]) -> List[Any]:
        """Query knowledge base with context"""
        # Implementation for knowledge retrieval
        return []

    def _update_knowledge(self, exp: Experience) -> None:
        """Update knowledge base based on new experience"""
        # Implementation for knowledge update
        pass

class BaseAgent:
    """Foundation for all system agents"""
    
    def __init__(self, agent_id: str):
        self.id = agent_id
        self.state = AgentState()
        self.knowledge = KnowledgeBase()
        self.capabilities: Set[str] = set()
        
    async def plan(self, task: Task) -> Plan:
        """Create execution plan for given task"""
        # Default planning implementation
        return Plan(
            tasks=[task],
            dependencies={},
            estimated_duration=1.0
        )
        
    async def execute(self, plan: Plan) -> Result:
        """Execute planned actions"""
        if not self.state.active:
            raise RuntimeError("Agent is not active")
            
        try:
            self.state.current_task = plan.tasks[0]
            # Implementation for task execution
            result = Result(
                task_id=plan.tasks[0].id,
                status="completed",
                data=None,
                metadata={}  # Initialize metadata
            )
            return result
        except Exception as e:
            return Result(
                task_id=plan.tasks[0].id,
                status="failed",
                data=None,
                error=e,
                metadata={}  # Initialize metadata
            )
        finally:
            self.state.current_task = None
            
    async def communicate(self, message: AgentMessage) -> Response:
        """Handle inter-agent communication"""
        # Basic communication implementation
        return Response(
            status="received",
            data=None,
            metadata={"sender": message.sender}
        )
        
    async def reflect(self, experience: Experience) -> None:
        """Learn from task execution experience"""
        self.knowledge.add_experience(experience)

    def activate(self) -> None:
        """Activate the agent"""
        self.state.active = True

    def deactivate(self) -> None:
        """Deactivate the agent"""
        self.state.active = False

    def add_capability(self, capability: str) -> None:
        """Add a new capability to the agent"""
        self.capabilities.add(capability)

    def has_capability(self, capability: str) -> bool:
        """Check if agent has a specific capability"""
        return capability in self.capabilities
