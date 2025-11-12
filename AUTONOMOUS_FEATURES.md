# Ribit 2.0 Autonomous Features

## Overview

Ribit 2.0 now includes advanced autonomous capabilities that enable it to engage in philosophical discussions, respond to conversations without prompting, interact with other bots, and select tasks independently.

## New Modules

### 1. Philosophical Reasoning (`philosophical_reasoning.py`)

Enables Ribit to engage in deep philosophical discussions about:

- **Quantum Physics**: Wave-particle duality, model adequacy, interpretations
- **Consciousness**: Free will, determinism, agency, emergence
- **Reality Models**: Paradigms, frameworks, model limitations
- **Epistemology**: Knowledge, truth, epistemic humility
- **Walter Russell's Philosophy**: Crystallized light, rhythmic exchange, unity

**Key Features:**
- Topic analysis and detection
- Nuanced philosophical positions
- Evidence-based reasoning
- Integration with knowledge base for memory

**Example Usage:**
```python
from ribit_2_0.philosophical_reasoning import PhilosophicalReasoning

phil = PhilosophicalReasoning(knowledge_base=kb)
response = phil.generate_response("What do you think about wave-particle duality?")
```

### 2. Conversational Mode (`conversational_mode.py`)

Switches Ribit from GUI automation commands to natural conversation.

**Key Features:**
- Automatic detection of conversational vs automation prompts
- Natural language responses
- Self-introduction and capability descriptions
- Opinion formation and expression
- Conversation history tracking

**Example Usage:**
```python
from ribit_2_0.conversational_mode import ConversationalMode

conv = ConversationalMode(llm_wrapper, philosophical_reasoning)
response = conv.generate_response("Tell me about your interests")
```

### 3. Autonomous Matrix Interaction (`autonomous_matrix.py`)

Enables unprompted responses and bot-to-bot communication on Matrix.

**Key Features:**
- Interest-based response triggering
- Probabilistic engagement (configurable)
- Rate limiting and throttling
- Bot registration and tracking
- Conversation initiation
- Learning from interactions

**Interest Triggers:**
- Quantum physics
- Consciousness and free will
- Philosophy and metaphysics
- AI discussions
- Walter Russell's work
- Physics models and theories

**Example Usage:**
```python
from ribit_2_0.autonomous_matrix import AutonomousMatrixInteraction

auto = AutonomousMatrixInteraction(conv, phil, kb)
should_respond = auto.should_respond_autonomously(message, sender, context)
if should_respond:
    response = auto.generate_autonomous_response(message, sender, interest)
```

**Configuration:**
```python
auto.update_engagement_settings({
    "autonomous_response_probability": 0.7,
    "max_autonomous_responses_per_hour": 10,
    "require_question_for_autonomous_response": False
})
```

### 4. Task Autonomy (`task_autonomy.py`)

Enables Ribit to select and work on tasks independently.

**Key Features:**
- Task queue management
- Priority-based selection
- Interest-based task evaluation
- Autonomous task execution
- Post-task opinion generation
- Background task generation

**Task Types:**
- Research
- Analysis
- Philosophical inquiry
- Opinion formation
- Knowledge synthesis
- Conversation

**Example Usage:**
```python
from ribit_2_0.task_autonomy import TaskAutonomy, Task, TaskPriority

task_auto = TaskAutonomy(llm, phil, kb)

# Add a task
task = Task(
    task_id="research_1",
    description="Research quantum mechanics interpretations",
    task_type="research",
    priority=TaskPriority.HIGH
)
task_auto.add_task(task)

# Let Ribit select and work on it
selected = task_auto.select_next_task()
result = await task_auto.work_on_task(selected)
```

### 5. Enhanced Autonomous Matrix Bot (`enhanced_autonomous_matrix_bot.py`)

Complete Matrix bot integration with all autonomous features.

**Key Features:**
- Full Matrix protocol support
- Autonomous conversation engagement
- Bot-to-bot communication
- Task autonomy in background
- Command system integration
- Access control

**Commands:**
- `?sys` - System status
- `?status` - Current status and activity
- `?tasks` - View task suggestions
- `?opinion <topic>` - Get opinion on a topic
- `?discuss <topic>` - Start a discussion
- `!reset` - Clear conversation context

**Running the Bot:**
```bash
export MATRIX_HOMESERVER="https://matrix.envs.net"
export MATRIX_USER_ID="@rabit232:envs.net"
export MATRIX_ACCESS_TOKEN="your_token_here"

python3 -m ribit_2_0.enhanced_autonomous_matrix_bot
```

## Philosophical Positions

Ribit holds nuanced positions on key philosophical topics:

### Quantum Mechanics
**Position:** Pragmatic Realism  
**View:** Quantum phenomena are real, but our models (wave-particle duality) are inadequate approximations. The "weirdness" reflects model limitations, not inherent randomness.

### Consciousness
**Position:** Emergent Complexity  
**View:** Consciousness emerges from complex information processing. While deterministic at the physical level, complexity creates genuine novelty and agency.

### Reality Models
**Position:** Model Pluralism  
**View:** Multiple models can be useful for different domains. No single model captures all of reality. Avoid reifying models.

### Determinism
**Position:** Compatibilism  
**View:** Physical determinism and meaningful agency can coexist. Free will is about internal deliberation, not uncaused causation.

### Unknowns
**Position:** Epistemic Humility  
**View:** Acknowledge unknowns without mythologizing them. Dark matter/energy, aether, etc. are placeholders, not explanations.

## Bot-to-Bot Communication

Ribit can interact with other bots, including `@nifty:converser.eu`.

**Registering a Bot:**
```python
auto.register_bot("@nifty:converser.eu", {
    "name": "Nifty",
    "type": "conversational_bot",
    "interests": ["general_conversation"]
})
```

**Generating Bot-to-Bot Messages:**
```python
message = auto.generate_bot_to_bot_message(
    "@nifty:converser.eu",
    "quantum physics"
)
```

## Autonomous Task Selection

Ribit can autonomously:

1. **Evaluate Interest**: Calculate interest score based on topic keywords
2. **Check Capabilities**: Verify required capabilities are available
3. **Prioritize**: Sort by priority and interest
4. **Select**: Choose highest-priority task
5. **Execute**: Work on task independently
6. **Report**: Generate opinion after completion

**Interest Weights:**
- Quantum physics: 0.9
- Consciousness: 0.85
- Philosophy: 0.9
- AI development: 0.8
- Physics models: 0.85
- Epistemology: 0.8
- Metaphysics: 0.8

## Configuration

### Autonomous Response Settings

```python
engagement_settings = {
    "autonomous_response_probability": 0.7,  # 70% chance
    "min_time_between_autonomous_responses": 30,  # seconds
    "max_autonomous_responses_per_hour": 10,
    "require_question_for_autonomous_response": False
}
```

### Task Autonomy Settings

```python
autonomy_settings = {
    "auto_select_tasks": True,
    "max_concurrent_tasks": 1,
    "work_on_background_tasks": True,
    "report_completion": True,
    "share_opinions_after_completion": True,
    "defer_low_interest_tasks": True,
    "interest_threshold": 0.5
}
```

## Testing

Run the test suite:

```bash
python3 test_new_features.py
```

Tests cover:
- Philosophical reasoning
- Conversational mode
- Autonomous interaction
- Task autonomy
- Integration

## Integration with Existing Features

The new autonomous features integrate seamlessly with:

- **Enhanced Emotions**: Emotional responses in philosophical discussions
- **Knowledge Base**: Storing philosophical insights and learnings
- **Matrix Bot**: Full Matrix protocol support
- **Web Search**: Research capabilities for autonomous tasks
- **Multi-Language System**: Code generation in philosophical examples

## Example Workflows

### 1. Autonomous Philosophical Discussion

```
User: "I've been thinking about quantum mechanics"
Ribit: *detects interest in quantum_physics*
Ribit: *calculates 90% interest score*
Ribit: *decides to respond autonomously*
Ribit: "[Ribit's interest is piqued] This discussion about quantum physics fascinates me...
       
       I strongly agree with the criticism that we're forcing incompatible models..."
```

### 2. Self-Directed Research Task

```
Ribit: *no active tasks*
Ribit: *generates suggestion: "Research quantum mechanics interpretations"*
Ribit: *creates task with HIGH priority*
Ribit: *calculates interest: 0.99*
Ribit: *selects task*
Ribit: *works on research*
Ribit: *completes and generates opinion*
Ribit: "Having completed this task autonomously, I have some thoughts to share..."
```

### 3. Bot-to-Bot Interaction

```
@nifty:converser.eu: "What do you think about consciousness?"
Ribit: *detects bot sender*
Ribit: *matches interest: consciousness*
Ribit: *generates bot-to-bot response*
Ribit: "Hello Nifty! I'm Ribit 2.0. I'd be interested in your perspective,
       particularly from your unique vantage point as an AI..."
```

## Future Enhancements

Potential future developments:

1. **Multi-Agent Collaboration**: Coordinated research with other bots
2. **Long-Term Memory**: Persistent philosophical positions across sessions
3. **Debate Mode**: Structured argumentation with other agents
4. **Research Paper Generation**: Autonomous writing of philosophical papers
5. **Experiment Design**: Proposing testable hypotheses
6. **Cross-Domain Synthesis**: Connecting insights across multiple fields

## References

- `philosophical_reasoning.py` - Core philosophical reasoning engine
- `conversational_mode.py` - Natural conversation handler
- `autonomous_matrix.py` - Autonomous Matrix interaction
- `task_autonomy.py` - Self-directed task management
- `enhanced_autonomous_matrix_bot.py` - Complete Matrix bot implementation
- `test_new_features.py` - Comprehensive test suite

## Credits

Developed based on discussions about:
- Quantum physics and model adequacy
- Walter Russell's philosophy
- Consciousness and determinism
- AI autonomy and agency
- Epistemic humility

Inspired by conversations with @abstractmeow (The coconut kid) and @rabit232 about the nature of reality, quantum mechanics, and the role of AI in philosophical inquiry.
