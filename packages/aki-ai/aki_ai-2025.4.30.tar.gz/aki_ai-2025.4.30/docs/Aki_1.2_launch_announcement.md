🚀 Aki 1.2: Easy Installation & Create Your Own Agents

We're thrilled to announce Aki 1.2! This release makes Aki more accessible with one-command installation and introduces the ability to create your own specialized agents. Plus, we've pre-installed AmazonInternalMCPServer for you to access amazon internal resources much easier.

## Major Updates

### One-Command Installation via Toolbox
Thanks to @songchao's amazing work, getting started with Aki is now as simple as:
```bash
toolbox registry add s3://aki-registry-bucket-us-west-2/tools.json && toolbox install aki
```
That's it! 

### Create Your Own Agents
Want an agent specialized for your specific needs? Now you can create one with a simple JSON profile:
```json
{
  "name": "MyAgent",
  "description": "My specialized assistant",
  "system_prompt": "You are an expert in...",
  "tools": ["file_management_readonly", "web_search"]
}
```
Just save your profile under `~/.aki/profiles/` and bring your custom agent to life! Check out our [Custom Profiles Guide](https://code.amazon.com/packages/Aki/blobs/heads/mainline/--/docs/custom_profiles.md) for more examples.

### Native Amazon Internal Integration
Seamlessly access Amazon's internal resources through our new AmazonInternalMCPServer:
- Browse internal websites with automatic Midway authentication
- Search across internal documentation and resources
- Quick access to Amazon code repositories

Learn more about MCP integration in our [MCP Guide](https://code.amazon.com/packages/Aki/blobs/heads/mainline/--/docs/mcp_guide.md).

## Special Thanks
- @locheng for adding Ollama model provider and DeepSeek models support
- @wanhuqi for polishing tools output format and improving the stop button functionality
- @takaro for fixing a connection bug between Aki and external MCP servers
- @xxxiao for improving aki documentation and prompts
- @shrsahi for adding support for ada profiles

## 📚 Getting Started

Check out our updated [README](https://code.amazon.com/packages/Aki/blobs/heads/mainline/--/README.md) for detailed documentation and examples. 