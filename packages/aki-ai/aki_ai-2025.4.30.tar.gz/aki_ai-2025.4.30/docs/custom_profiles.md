# Project migrated to AMZN_AKI
# Check docs under https://code.amazon.com/packages/AMZN_AKI/blobs/mainline/--/docs/ for the latest version

# Creating Custom Profiles in Aki

Aki introduces a powerful way to create your own specialized AI agents using simple JSON configuration. This guide will help you create and customize your own Aki agents.

## Quick Start

1. Create a profile JSON file in `~/.aki/profiles/my_agent.json`:
```json
{
  "name": "MyAgent",
  "description": "My specialized assistant",
  "system_prompt": "You are an expert in...",
  "tools": [
    "file_management_readonly",
    "web_search"
  ],
  "enabled_mcp_servers": ["internal-amazon-server"],
  "default_model": "(aws)us.anthropic.claude-3-7-sonnet-20250219-v1:0",
  "reasoning_config": {
    "default_enabled": true,
    "budget_tokens": 4096
  },
  "starters": [
    {
      "label": "Start Task",
      "message": "What can I help you with?"
    }
  ]
}
```

2. Launch Aki and select your agent from the profile list!

## Profile Configuration

### Location
Place your profile files in either:
- `~/.aki/profiles/` (recommended for user profiles)

### Profile Schema
```json
{
  "name": "Display Name",
  "description": "What the agent does",
  "default": false,
  "order_id": 15,  // Optional ordering value (smaller numbers appear first)
  "system_prompt": "Inline system prompt...",
  // OR use a file:
  // "system_prompt_file": "prompts/agent.txt",
  // Rules file for operational guidelines:
  // "rules_file": "prompts/agent_rule.txt",
  "tools": ["tool1", "tool2"],
  "enabled_mcp_servers": "__ALL__",  // or ["server1", "server2"]
  "default_model": "(aws)us.anthropic.claude-3-7-sonnet-20250219-v1:0",  // Optional
  "reasoning_config": {  // Optional
    "default_enabled": true,
    "budget_tokens": 4096
  },
  "starters": [
    {
      "label": "Button Label",
      "message": "What to send when clicked",
      "icon": "Optional icon URL"
    }
  ]
}
```

## Available Tools

### Tool Collections
- `file_management_full`: Complete file operations (read/write/delete)
- `file_management_readonly`: Safe read-only file operations

### Individual Tools
- `shell_command`: Execute shell commands
- `browser_action`: Control browser for web interaction
- `render_html`: Display HTML content
- `code_analyzer`: Analyze code structure
- `python_executor`: Execute Python code
- `web_search`: Search the web
- `tasklist`: Manage task lists
- `get_datetime_now`: Get current time
- `process_manager`: Run and monitor long-running processes

### Built-in MCP Servers
- "internal-amazon-server":
  - `read_internal_website`: Access internal Amazon sites
  - `search_internal_websites`: Search internal documentation
  - `search_internal_code`: Search Amazon code repositories

## Model Configuration

### Available Models

Specify your preferred model using the `default_model` field:

```json
{
  "default_model": "(aws)us.anthropic.claude-3-7-sonnet-20250219-v1:0"
}
```

Common model options:
- `(aws)us.anthropic.claude-3-7-sonnet-20250219-v1:0` - Claude 3.7 Sonnet
- `(aws)us.anthropic.claude-3-5-sonnet-20241022-v2:0"` - Claude 3.5 Sonnet
- `(aws)us.anthropic.claude-3-5-haiku-20241022-v1:0` - Claude 3.5 Haiku

### Reasoning Configuration

Control how the model uses its reasoning capabilities:

```json
{
  "reasoning_config": {
    "default_enabled": true,  // Enable extended reasoning by default
    "budget_tokens": 4096     // Maximum tokens for reasoning steps
  }
}
```

## System Prompts and Rules

You can define the agent's behavior and operational guidelines using prompts and rules:

### System Prompts

#### 1. Inline Prompt
```json
{
  "system_prompt": "You are an expert in..."
}
```

#### 2. File Reference
```json
{
  "system_prompt_file": "prompts/my_agent.txt"
}
```

### Rules Files

Rules files provide operational guidelines that dictate how the agent should behave, such as task management practices, tool usage patterns, and response formatting:

```json
{
  "rules_file": "prompts/my_agent_rule.txt"
}
```

A rules file typically uses the `<rule>...</rule>` format and contains specific operational instructions:

```text
<rule>
1. Task Management:
   - Always use batch_tool for efficiency
   - Keep users informed with task status updates
   - Break down complex problems into manageable tasks

2. Tool Usage:
   - Use specific patterns for tool operations
   - Implement safety checks before file modifications

3. Response Formatting:
   - Follow specific citation formats
   - Structure answers consistently
</rule>
```

### Prompt Structure
```text
<role_definition>
Define the agent's primary role and expertise
</role_definition>

<capabilities>
List specific capabilities and skills
</capabilities>

<instructions>
Provide detailed instructions for:
1. Task handling approach
2. Tool usage guidelines
3. Response formatting
</instructions>
```

## Example Profiles

### 1. Internal Documentation Assistant with Claude 3.7 and Rules
```json
{
  "name": "Doc Assistant",
  "description": "Helps navigate Amazon internal documentation",
  "order_id": 5,  // Will appear before Aki (which has order_id 10)
  "system_prompt": "You are an expert in Amazon's internal documentation...",
  "rules_file": "prompts/doc_assistant_rule.txt",
  "tools": [
    "file_management_readonly",
    "web_search",
    "batch_tool",
    "tasklist"
  ],
  "enabled_mcp_servers": ["internal-amazon-server"],
  "default_model": "(aws)us.anthropic.claude-3-7-sonnet-20250219-v1:0",
  "reasoning_config": {
    "default_enabled": true,
    "budget_tokens": 4096
  },
  "starters": [
    {
      "label": "Search Docs",
      "message": "I need help finding documentation about..."
    },
    {
      "label": "Code Search",
      "message": "Can you help me find code related to..."
    }
  ]
}
```

### 2. Development Helper with Process Management
```json
{
  "name": "Dev Helper",
  "description": "Your coding assistant with server management",
  "order_id": 15,  // Will appear between Aki (10) and Akira (20)
  "system_prompt_file": "prompts/dev_helper.txt",
  "tools": [
    "code_analyzer",
    "python_executor",
    "file_management_readonly",
    "process_manager"
  ],
  "enabled_mcp_servers": "__ALL__",
  "default_model": "(aws)us.anthropic.claude-3-sonnet-20240229-v1:0",
  "starters": [
    {
      "label": "Analyze Code",
      "message": "Can you analyze this code..."
    },
    {
      "label": "Start Server",
      "message": "Can you start a development server for me..."
    }
  ]
}
```

## Profile Ordering

You can control the order in which profiles appear in the UI by using the `order_id` field:

```json
{
  "name": "My Custom Agent",
  "description": "My specialized profile",
  "order_id": 5,  // Will appear between profiles with order 5 and 6
  // other configuration...
}
```

### Profile Order Rules

1. **Lower numbers appear first** in the profile selection list
2. Built-in profiles have these default order values:
   - Aki: 10
   - Aki Team: 40
   - Akira: 20
   - Akisa: 30
   - Custom profiles without `order_id`: 100
3. You can use **negative numbers** or **decimal values** (like 9.5) to position your profile precisely
4. All profiles are sorted strictly by their `order_id` value, including the default profile

### Default Profile vs. Order

The `default` and `order_id` fields serve different purposes:

- `"default": true` - Determines which profile is automatically selected when Aki starts
- `"order_id": value` - Controls where the profile appears in the selection list

If you want a profile to be both default AND appear first in the list, you need both:
```json
{
  "name": "My Default Profile",
  "default": true,
  "order_id": 1,  // Lower than built-in profiles
  // other settings...
}
```

### Examples

- `"order_id": 1` - Appears before all built-in profiles
- `"order_id": 15` - Appears between Aki (10) and Akira (20)

## Best Practices

1. **Tool Selection**
   - Start with `file_management_readonly` for safety
   - Only enable tools your agent needs
   - Use `enabled_mcp_servers` to control external tool access

2. **System Prompts and Rules**
   - Be specific about the agent's role in system prompts
   - Use rules files for operational guidelines and behavior standards
   - Define clear task management patterns in rules files
   - Include specific tool usage instructions and formatting requirements

3. **Model Selection**
   - Use Claude 3.7 for complex reasoning tasks
   - Configure reasonable token budgets for reasoning
   - Consider task complexity when selecting models

4. **Starters**
   - Create task-specific starter buttons
   - Use clear, action-oriented labels
   - Include common use-case messages

## Important Notes

1. Profile names must be unique
2. Invalid tool names are ignored
3. System prompts should align with enabled tools
4. Built-in profiles cannot be overridden
5. Changes require Aki restart to take effect

For advanced multi-agent profiles using Python, see the [Development Guide](development_guide.md).