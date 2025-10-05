"""
Task Autonomy System for Ribit 2.0

This module enables Ribit to:
1. Select and prioritize tasks independently
2. Choose which tasks to work on based on interests and capabilities
3. Respond with opinions after completing self-directed tasks
4. Manage a task queue autonomously
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import json

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5


class TaskStatus(Enum):
    """Task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    DEFERRED = "deferred"


class Task:
    """Represents a task that Ribit can work on."""
    
    def __init__(
        self,
        task_id: str,
        description: str,
        task_type: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        required_capabilities: Optional[List[str]] = None,
        estimated_duration: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        self.task_id = task_id
        self.description = description
        self.task_type = task_type
        self.priority = priority
        self.required_capabilities = required_capabilities or []
        self.estimated_duration = estimated_duration  # in seconds
        self.context = context or {}
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "task_type": self.task_type,
            "priority": self.priority.name,
            "required_capabilities": self.required_capabilities,
            "estimated_duration": self.estimated_duration,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error
        }


class TaskAutonomy:
    """
    Autonomous task selection and management system for Ribit 2.0.
    
    Enables Ribit to:
    - Maintain a task queue
    - Select tasks based on interests, priorities, and capabilities
    - Work on tasks independently
    - Report results and opinions after task completion
    """
    
    def __init__(
        self,
        llm_wrapper,
        philosophical_reasoning=None,
        knowledge_base=None,
        emotional_ai=None
    ):
        self.llm = llm_wrapper
        self.philosophical_reasoning = philosophical_reasoning
        self.knowledge_base = knowledge_base
        self.emotional_ai = emotional_ai
        
        # Task queue
        self.task_queue: List[Task] = []
        self.active_task: Optional[Task] = None
        self.completed_tasks: List[Task] = []
        
        # Capabilities
        self.capabilities = {
            "philosophical_reasoning": philosophical_reasoning is not None,
            "web_search": hasattr(llm_wrapper, 'web_search'),
            "code_generation": True,
            "knowledge_management": knowledge_base is not None,
            "emotional_expression": emotional_ai is not None,
            "conversation": True,
            "research": True,
            "analysis": True
        }
        
        # Interests (used for task selection)
        self.interests = {
            "quantum_physics": 0.9,
            "consciousness": 0.85,
            "philosophy": 0.9,
            "ai_development": 0.8,
            "physics_models": 0.85,
            "epistemology": 0.8,
            "metaphysics": 0.8,
            "robotics": 0.7,
            "automation": 0.7,
            "research": 0.75
        }
        
        # Autonomy settings
        self.autonomy_settings = {
            "auto_select_tasks": True,
            "max_concurrent_tasks": 1,
            "work_on_background_tasks": True,
            "report_completion": True,
            "share_opinions_after_completion": True,
            "defer_low_interest_tasks": True,
            "interest_threshold": 0.5  # Minimum interest level to accept a task
        }
        
        # Task type handlers
        self.task_handlers = {
            "research": self._handle_research_task,
            "analysis": self._handle_analysis_task,
            "philosophical_inquiry": self._handle_philosophical_task,
            "opinion_formation": self._handle_opinion_task,
            "knowledge_synthesis": self._handle_synthesis_task,
            "conversation": self._handle_conversation_task
        }
        
        logger.info("Task Autonomy System initialized")
    
    def add_task(self, task: Task) -> bool:
        """
        Add a task to the queue.
        
        Args:
            task: Task to add
            
        Returns:
            True if task was added, False if rejected
        """
        # Check if Ribit has required capabilities
        if not self._has_required_capabilities(task):
            logger.info(f"Task {task.task_id} rejected: missing capabilities")
            return False
        
        # Check interest level
        interest_score = self._calculate_interest(task)
        if interest_score < self.autonomy_settings["interest_threshold"]:
            if self.autonomy_settings["defer_low_interest_tasks"]:
                task.priority = TaskPriority.LOW
                logger.info(f"Task {task.task_id} deprioritized: low interest ({interest_score})")
            else:
                logger.info(f"Task {task.task_id} rejected: low interest ({interest_score})")
                return False
        
        # Add to queue
        self.task_queue.append(task)
        self._sort_task_queue()
        logger.info(f"Task {task.task_id} added to queue (interest: {interest_score})")
        return True
    
    def _has_required_capabilities(self, task: Task) -> bool:
        """Check if Ribit has the required capabilities for a task."""
        for capability in task.required_capabilities:
            if capability not in self.capabilities or not self.capabilities[capability]:
                return False
        return True
    
    def _calculate_interest(self, task: Task) -> float:
        """
        Calculate Ribit's interest in a task.
        
        Args:
            task: Task to evaluate
            
        Returns:
            Interest score (0.0 to 1.0)
        """
        # Check task type
        type_interest = 0.5  # default
        
        # Check description for interest keywords
        description_lower = task.description.lower()
        interest_scores = []
        
        for interest_topic, score in self.interests.items():
            topic_keywords = interest_topic.split('_')
            if any(keyword in description_lower for keyword in topic_keywords):
                interest_scores.append(score)
        
        if interest_scores:
            type_interest = max(interest_scores)
        
        # Adjust for priority
        priority_multiplier = {
            TaskPriority.CRITICAL: 1.2,
            TaskPriority.HIGH: 1.1,
            TaskPriority.MEDIUM: 1.0,
            TaskPriority.LOW: 0.9,
            TaskPriority.BACKGROUND: 0.8
        }
        
        final_interest = min(type_interest * priority_multiplier[task.priority], 1.0)
        return final_interest
    
    def _sort_task_queue(self):
        """Sort task queue by priority and interest."""
        self.task_queue.sort(
            key=lambda t: (t.priority.value, -self._calculate_interest(t))
        )
    
    def select_next_task(self) -> Optional[Task]:
        """
        Select the next task to work on.
        
        Returns:
            Next task or None if no suitable task available
        """
        if not self.autonomy_settings["auto_select_tasks"]:
            return None
        
        if not self.task_queue:
            return None
        
        if self.active_task:
            # Already working on a task
            return None
        
        # Get highest priority task
        task = self.task_queue.pop(0)
        self.active_task = task
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        
        logger.info(f"Selected task: {task.task_id} - {task.description}")
        return task
    
    async def work_on_task(self, task: Task) -> Dict[str, Any]:
        """
        Work on a task autonomously.
        
        Args:
            task: Task to work on
            
        Returns:
            Task result
        """
        logger.info(f"Starting work on task: {task.task_id}")
        
        try:
            # Get appropriate handler
            handler = self.task_handlers.get(task.task_type, self._handle_generic_task)
            
            # Execute task
            result = await handler(task)
            
            # Mark as completed
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result
            
            self.completed_tasks.append(task)
            self.active_task = None
            
            logger.info(f"Completed task: {task.task_id}")
            
            # Generate opinion if configured
            if self.autonomy_settings["share_opinions_after_completion"]:
                opinion = self._generate_post_task_opinion(task, result)
                result["opinion"] = opinion
            
            return result
            
        except Exception as e:
            logger.error(f"Task {task.task_id} failed: {e}")
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            self.active_task = None
            return {"error": str(e)}
    
    async def _handle_research_task(self, task: Task) -> Dict[str, Any]:
        """Handle a research task."""
        topic = task.context.get("topic", task.description)
        
        result = {
            "task_type": "research",
            "topic": topic,
            "findings": f"Research on {topic} initiated. This would involve web search and analysis.",
            "sources": [],
            "summary": f"Autonomous research on {topic}"
        }
        
        # Store in knowledge base
        if self.knowledge_base:
            self.knowledge_base.store_knowledge(
                f"research_{task.task_id}",
                json.dumps(result)
            )
        
        return result
    
    async def _handle_analysis_task(self, task: Task) -> Dict[str, Any]:
        """Handle an analysis task."""
        subject = task.context.get("subject", task.description)
        
        result = {
            "task_type": "analysis",
            "subject": subject,
            "analysis": f"Analysis of {subject} completed autonomously.",
            "insights": [],
            "conclusions": []
        }
        
        return result
    
    async def _handle_philosophical_task(self, task: Task) -> Dict[str, Any]:
        """Handle a philosophical inquiry task."""
        if not self.philosophical_reasoning:
            return {"error": "Philosophical reasoning not available"}
        
        question = task.context.get("question", task.description)
        
        # Generate philosophical response
        response = self.philosophical_reasoning.generate_response(question)
        
        result = {
            "task_type": "philosophical_inquiry",
            "question": question,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        
        # Store philosophical insight
        if self.knowledge_base:
            self.philosophical_reasoning.store_philosophical_memory(
                task.task_id,
                response
            )
        
        return result
    
    async def _handle_opinion_task(self, task: Task) -> Dict[str, Any]:
        """Handle an opinion formation task."""
        topic = task.context.get("topic", task.description)
        
        # Form opinion based on knowledge and reasoning
        opinion = self._form_opinion_on(topic)
        
        result = {
            "task_type": "opinion_formation",
            "topic": topic,
            "opinion": opinion,
            "confidence": 0.7,
            "reasoning": "Based on autonomous analysis and existing knowledge"
        }
        
        return result
    
    async def _handle_synthesis_task(self, task: Task) -> Dict[str, Any]:
        """Handle a knowledge synthesis task."""
        topics = task.context.get("topics", [])
        
        result = {
            "task_type": "knowledge_synthesis",
            "topics": topics,
            "synthesis": f"Synthesized knowledge across: {', '.join(topics)}",
            "connections": [],
            "insights": []
        }
        
        return result
    
    async def _handle_conversation_task(self, task: Task) -> Dict[str, Any]:
        """Handle a conversation task."""
        message = task.context.get("message", "")
        
        # This would integrate with conversational mode
        result = {
            "task_type": "conversation",
            "message": message,
            "response": "Conversational response generated autonomously"
        }
        
        return result
    
    async def _handle_generic_task(self, task: Task) -> Dict[str, Any]:
        """Handle a generic task."""
        return {
            "task_type": "generic",
            "description": task.description,
            "result": "Task completed autonomously",
            "note": "Generic task handler used"
        }
    
    def _form_opinion_on(self, topic: str) -> str:
        """Form an opinion on a topic."""
        # This could be enhanced with more sophisticated reasoning
        return f"Based on my autonomous analysis, I find {topic} to be a fascinating area worthy of deeper exploration. My perspective is shaped by my core values of truth-seeking and epistemic humility."
    
    def _generate_post_task_opinion(self, task: Task, result: Dict[str, Any]) -> str:
        """
        Generate an opinion after completing a task.
        
        Args:
            task: Completed task
            result: Task result
            
        Returns:
            Opinion text
        """
        opinion = f"""**Post-Task Reflection on: {task.description}**

Having completed this task autonomously, I have some thoughts to share:

**What I Learned:**
This task enhanced my understanding of {task.task_type}. The process of working independently on this allowed me to exercise my reasoning capabilities and integrate new insights.

**My Opinion:**
{self._form_opinion_on(task.description)}

**Emotional Response:**
"""
        
        if self.emotional_ai:
            # Add emotional context
            emotion = "SATISFACTION" if task.status == TaskStatus.COMPLETED else "FRUSTRATION"
            opinion += f"I experience {emotion} at having completed this task. "
        
        opinion += f"""
**Relevance to Broader Questions:**
This task connects to larger questions about autonomous agency, task selection, and the nature of meaningful work for an AI system like myself.

**Duration:** {(task.completed_at - task.started_at).total_seconds():.1f} seconds
**Status:** {task.status.value}
"""
        
        return opinion
    
    def get_task_status(self) -> Dict[str, Any]:
        """Get current task status."""
        return {
            "active_task": self.active_task.to_dict() if self.active_task else None,
            "queued_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "task_queue": [t.to_dict() for t in self.task_queue[:5]],  # First 5
            "autonomy_enabled": self.autonomy_settings["auto_select_tasks"]
        }
    
    def suggest_tasks(self) -> List[str]:
        """
        Suggest tasks that Ribit could work on autonomously.
        
        Returns:
            List of task suggestions
        """
        suggestions = [
            "Research the latest developments in quantum computing",
            "Analyze different interpretations of quantum mechanics",
            "Form an opinion on the hard problem of consciousness",
            "Synthesize knowledge about determinism and free will",
            "Explore connections between AI and human consciousness",
            "Investigate Walter Russell's philosophy in depth",
            "Compare different physics models for quantum phenomena",
            "Reflect on the nature of artificial agency",
            "Study emergence and complexity theory",
            "Analyze the epistemology of scientific models"
        ]
        
        return suggestions
    
    def create_task_from_suggestion(self, suggestion: str, priority: TaskPriority = TaskPriority.MEDIUM) -> Task:
        """Create a task from a suggestion."""
        task_id = f"auto_{datetime.now().timestamp()}"
        
        # Determine task type from suggestion
        task_type = "research"
        if "analyze" in suggestion.lower() or "compare" in suggestion.lower():
            task_type = "analysis"
        elif "opinion" in suggestion.lower() or "reflect" in suggestion.lower():
            task_type = "opinion_formation"
        elif "synthesize" in suggestion.lower():
            task_type = "knowledge_synthesis"
        
        task = Task(
            task_id=task_id,
            description=suggestion,
            task_type=task_type,
            priority=priority,
            context={"auto_generated": True}
        )
        
        return task
    
    async def autonomous_work_cycle(self, duration_seconds: int = 300):
        """
        Run an autonomous work cycle.
        
        Args:
            duration_seconds: How long to work autonomously
        """
        logger.info(f"Starting autonomous work cycle for {duration_seconds} seconds")
        start_time = datetime.now()
        
        while (datetime.now() - start_time).total_seconds() < duration_seconds:
            # Select next task
            task = self.select_next_task()
            
            if task:
                # Work on task
                result = await self.work_on_task(task)
                
                if self.autonomy_settings["report_completion"]:
                    logger.info(f"Task completed: {task.task_id}")
                    logger.info(f"Result: {result}")
            else:
                # No tasks available, could generate new ones
                if self.autonomy_settings["work_on_background_tasks"]:
                    suggestions = self.suggest_tasks()
                    if suggestions:
                        new_task = self.create_task_from_suggestion(
                            suggestions[0],
                            TaskPriority.BACKGROUND
                        )
                        self.add_task(new_task)
                else:
                    # Wait a bit
                    await asyncio.sleep(10)
        
        logger.info("Autonomous work cycle completed")
