# Project migrated to AMZN_AKI
# Check docs under https://code.amazon.com/packages/AMZN_AKI/blobs/mainline/--/docs/ for the latest version

# Aki Development Guide

This guide covers setting up your development environment and creating advanced Python-based profiles for Aki.

## Configuration

### Environment Variables

Configuration is managed through environment variables in `.env` file. Copy `.env.example` to create your configuration:

```bash
cp src/amzn_aki/config/.env.example ~/.aki/.env
```

Available configurations:

| Variable | Description | Default | Valid Range |
|----------|-------------|---------|-------------|
| AKI_TOOL_TIME_OUT_THRESHOLD | Maximum time (seconds) for tool execution | 60 | > 0 |
| AKI_TOKEN_THRESHOLD | Maximum tokens before conversation summarization | 160000 | 30000-200000 |
| AWS_ACCESS_KEY_ID | AWS access key (if using AWS services) | - | - |
| AWS_SECRET_ACCESS_KEY | AWS secret key (if using AWS services) | - | - |

### Token Threshold Configuration

The `AKI_TOKEN_THRESHOLD` controls when Aki will automatically summarize the conversation to prevent context overflow:

- Default: 160000 tokens
- Minimum: 30000 token
- Maximum: 200000 tokens

When the conversation reaches this threshold:
1. Aki generates a summary of the conversation
2. Previous messages are replaced with the summary
3. Token count is reset
4. Conversation continues with the summary as context

Example configuration:
```bash
# Conservative setting (trigger summary earlier)
AKI_TOKEN_THRESHOLD=100000

# Maximum setting (allow longer conversations)
AKI_TOKEN_THRESHOLD=190000
```

## Development Setup

### 1. Create Workspace
```bash
brazil ws create -n Aki -vs Aki/development 
cd Aki/
brazil ws use -p Aki
```

### 2. Configure Python
Requires [mise](https://docs.hub.amazon.dev/brazil/peru-user-guide/python-peru/#peru-python-local-ws):
```bash
mise use -g python@3.12
cd ~/workplace/Aki/src/Aki
brazil-build
```

### 3. Launch Aki
```bash
brazil-build run server
```

## Integration Test
### Run Only Integration Tests
```bash
brazil-build run test_integration
```

### Run specific test:
```
brazil-build run pytest tests/integration/test_aki_profile.py -sv
```

Example output:
```
tests/integration/test_aki_profile.py::test_profile_registry_includes_aki PASSED
tests/integration/test_aki_profile.py::test_profile_factory_creates_aki PASSED
tests/integration/test_aki_profile.py::test_aki_conversation_basic - Last LLM call used tokens: 5401

----- ACTUAL LLM RESPONSE -----
Hi there! How can I help you today?
------------------------------
PASSED
```


## Advanced Profile Development

While simple agents can be created using JSON (see [Custom Profiles](custom_profiles.md)), complex multi-agent systems require Python implementation.

### Creating a Supervisor Profile

1. Create a new file `src/amzn_aki/chat/implementations/supervisor/my_team.py`:
```python
from typing import List, TypedDict
from chainlit import cl
from ....tools.router import create_router_tool
from ...base.base_profile import BaseProfile
from ...graph.supervisor_graph import SupervisorGraph, SupervisorConfig

class MyTeamState(TypedDict):
    current_task: str
    active_agents: List[str]

class MyTeamProfile(BaseProfile):
    def __init__(self):
        super().__init__()
        self._graph_handler = None
        
    @classmethod
    def name(cls) -> str:
        return "My Expert Team"
        
    @classmethod
    def chat_profile(cls) -> cl.ChatProfile:
        return cl.ChatProfile(
            name=cls.name(),
            markdown_description="A team of specialized agents that...",
            starters=[
                cl.Starter(
                    name="Start Project",
                    description="Begin a new project...",
                    message="I need help with..."
                )
            ]
        )
        
    def create_graph(self):
        """Create the supervisor graph with specialized agents."""
        if not self._graph_handler:
            config = SupervisorConfig(
                supervisor_node_name="Team Lead",
                agent_configs=[
                    {
                        "name": "Architect",
                        "role": "Design expert...",
                        "tools": ["code_analyzer"]
                    },
                    {
                        "name": "Developer",
                        "role": "Implementation expert...",
                        "tools": ["file_management_full"]
                    }
                ]
            )
            self._graph_handler = SupervisorGraph(config)
        return self._graph_handler.create_graph()
```

2. Register your profile in `src/amzn_aki/config/profile_manager.py`:
```python
def _load_profiles(self):
    # Existing code...
    
    from ..chat.implementations.supervisor.my_team import MyTeamProfile
    self.registry.register_supervisor_profile(
        "my_team",
        MyTeamProfile,
        order=50  # Controls menu order
    )
```

### Profile Components

#### SupervisorConfig
Controls the team structure and agent capabilities:
```python
SupervisorConfig(
    supervisor_node_name="Team Lead",
    agent_configs=[
        {
            "name": "Agent Name",
            "role": "Detailed role description",
            "tools": ["tool1", "tool2"],
            "memory": True  # Enable agent memory
        }
    ],
    shared_tools=["common_tool1"],  # Tools available to all agents
    enable_memory=True  # Enable team memory
)
```

#### Graph Handler
Manages agent communication and task flow:
```python
def create_graph(self):
    if not self._graph_handler:
        config = SupervisorConfig(...)
        self._graph_handler = SupervisorGraph(
            config,
            state_handler=self.handle_state_update,
            message_handler=self.handle_message
        )
    return self._graph_handler.create_graph()
```

## Best Practices

### 1. Profile Design
- Use JSON profiles for single agents
- Use Python profiles for multi-agent teams
- Keep agent roles focused and specific

### 2. State Management
- Define clear state interfaces with TypedDict
- Handle state updates explicitly
- Share state carefully between agents

### 3. Tool Usage
- Implement proper tool access control
- Document tool requirements
- Handle tool failures gracefully

### 4. Testing
- Test agent interactions
- Verify state management
- Validate tool permissions

## Troubleshooting

### Build Errors

#### Connection Error
Problem:
```
Caused by: error sending request for url (http://127.0.0.1:54686/...)
Caused by: client error (Connect)
```

Solution:
```bash
rm -r .hatch && brazil-build
```

#### Python Version Mismatch
Problem: Incompatible Python version

Solution:
```bash
mise use -g python@3.12
brazil-build clean
brazil-build
```

For more examples and detailed API documentation, check the source code in `src/amzn_aki/chat/implementations/`.