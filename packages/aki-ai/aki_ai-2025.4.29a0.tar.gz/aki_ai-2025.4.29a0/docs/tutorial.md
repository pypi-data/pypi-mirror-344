# Project migrated to AMZN_AKI
# Check docs under https://code.amazon.com/packages/AMZN_AKI/blobs/mainline/--/docs/ for the latest version

# Aki Tutorial: Advanced AI Assistance for Amazon SDEs

## Table of Contents
1. [Understanding AI Agents](#understanding-ai-agents)
2. [Tool-Augmented AI](#tool-augmented-ai)
3. [Multi-Agent Collaboration](#multi-agent-collaboration)
4. [Getting Started with Aki](#getting-started)
5. [Current Status and Future Roadmap](#roadmap)

## Understanding AI Agents

AI agents represent a significant evolution in how we interact with large language models (LLMs). According to research and industry practices, there are four key strategies that significantly improve LLM performance:

1. **Reflection**: Agents can examine their own work and identify improvements
2. **Tool Use**: Agents leverage external tools for enhanced capabilities
3. **Planning**: Agents create and execute multi-step plans to achieve complex goals
4. **Multi-agent Collaboration**: Multiple specialized agents work together for better outcomes

*Further Reading:* [How Agents Can Improve LLM Performance](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/?ref=dl-staging-website.ghost.io)

## Tool-Augmented AI

### Why Tools Matter?
While LLMs are powerful, they have limitations in handling real-world development tasks. Traditional chat interfaces require:
- Manual context copying and pasting
- Constant environment switching
- Limited access to development resources

Aki overcomes these limitations through integrated tools that allow direct interaction with:
- Code repositories
- File systems
- Development environments
- Web resources

#### How It Works
![alt text](<Workflow Graph: Aki - Ask me anything.png>) 

*Further Reading:* [Agentic Design Patterns: Tool Use](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-3-tool-use/?ref=dl-staging-website.ghost.io)

## Multi-Agent Collaboration

### The Power of Specialized Agents
Aki's multi-agent system distributes complex tasks across specialized agents:

- **Aki**: Team coordinator and task delegator
- **Akira**: Research and code analysis specialist
- **Akisa**: Implementation and file management expert
- **Akipy**: Python development specialist
- **Akita**: Testing specialist (Coming Soon)
- **Akido**: Documentation expert (Coming Soon)

### Demo: Test-Driven Development
Example workflow:
1. Aki coordinates the overall development process
2. Akira researches implementation approaches
3. Akita develops test suites
4. Akisa implements the solution
5. Team collaborates on review and refinement

![alt text](<Workflow Graph: Aki team - Chat with professionals.png>)

*Further Reading:* 
- [Agentic Design Patterns: Multi-Agent Collaboration](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-5-multi-agent-collaboration/?ref=dl-staging-website.ghost.io)
- [Multi-agent supervisor](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/)

## Getting Started

### Current Availability
- Released Production: [AutoSDE](https://w.amazon.com/bin/view/AutoSDE/)
- Early Access: [Aki](https://code.amazon.com/packages/Aki/trees/mainline)

### Why Now?
- Latest LLM models optimized for tool use
- Proven effectiveness of agentic workflows
- Growing need for integrated AI development assistance
- Bridge between internal tools and industry-leading solutions

## Roadmap

### Coming Soon
1. **Enhanced Team Capabilities**
   - Additional specialized agents
   - Expanded tool integrations
   - Improved inter-agent coordination

2. **Advanced Features**
   - Conversation history and memory support
   - Optimized workflows for code analysis
   - Enhanced unit test generation capabilities
   - Improved tech documentation generation

3. **Integration Improvements**
   - Enhanced Amazon internal tools support
   - Expanded language and framework support

---

*Note: This tutorial is continuously updated as new features and capabilities are added to the Aki family of tools.*
