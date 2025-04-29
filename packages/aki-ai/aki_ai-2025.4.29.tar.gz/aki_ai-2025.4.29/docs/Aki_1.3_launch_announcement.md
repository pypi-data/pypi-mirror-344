🚀 Aki 1.3: Extended Reasoning, Persistent Memory & Improved Tools

We're thrilled to announce Aki 1.3! This release brings powerful reasoning capabilities with Claude 3.7 and DeepSeek-R1, persistent conversations, and significant tooling improvements to help you tackle complex development tasks with greater efficiency.

## Major Updates

### Claude 3.7 / DeepSeek-R1 Integration with Extended Reasoning
- Step-by-step problem solving with configurable reasoning depth
- More coherent solutions for complex technical challenges
- Reasoning budget control for optimal performance
```json
"reasoning_config": {
  "default_enabled": true,
  "budget_tokens": 4096
}
```

### Persistent Chat History
- Conversations automatically saved to local databases
- Resume work exactly where you left off days or weeks later
- Configure in your environment settings with simple database URL

### Smart Conversation Management
- Handles longer than 200k tokens while maintaining context
- Automatic summarization of long conversations preserving key details
- Better tracking of workspace changes during long sessions

### Process Manager for Development Workflows
A powerful new tool for managing long-running processes:
```
# Start a development server and get initial output
process_manager start "python -m http.server 8000"

# Get latest output
process_manager output process_id=12345

# Terminate when done
process_manager terminate process_id=12345
```

### Conversation Export Options
- Export sessions in JSON, Markdown, or plaintext for documentation
- Properly formatted interactions including tool usage
- Perfect for knowledge sharing and documentation

### Custom Profiles
Quick setup for specialized workflows:
```json
{
  "name": "DevOps-Aki",
  "description": "DevOps specialized assistant",
  "tools": ["file_management_full", "process_manager", "web_search"]
}
```
Check out our [onboarding profile for full-CD pipeline use cases](https://code.amazon.com/packages/AkiSharedCustomerProfiles/blobs/mainline/--/profiles/full-cd-assistant.json).

### Enhanced MCP Integration
- More robust MCP server installation script
- Simplified setup process for extending Aki with custom tools

## 📚 Getting Started

Check out our updated [README](https://code.amazon.com/packages/Aki/blobs/heads/mainline/--/README.md) for detailed documentation and examples.

Join our [#aki-interest](https://amazon.enterprise.slack.com/archives/C089A4NAG9K) Slack channel to share your experiences or learn more about maximizing Aki's capabilities!