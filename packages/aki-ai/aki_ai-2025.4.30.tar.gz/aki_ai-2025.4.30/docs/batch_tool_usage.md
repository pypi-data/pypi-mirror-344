# Batch Tool Usage Guide

The Batch Tool allows executing multiple tools in a single API call, reducing latency and improving user experience.

## Input Format

The batch_tool requires a list of `invocations`, each containing:
1. `name`: The name of the tool to invoke
2. `arguments`: A dictionary of arguments for that tool

## Examples

### Basic Example

```json
{
  "invocations": [
    {
      "name": "read_file",
      "arguments": {
        "file_path": "README.md"
      }
    },
    {
      "name": "file_search",
      "arguments": {
        "pattern": "*.py",
        "dir_path": "src"
      }
    }
  ]
}
```

### Combining Think Tool with Other Operations

```json
{
  "invocations": [
    {
      "name": "think",
      "arguments": {
        "thought": "Analyzing the file structure to understand the project organization."
      }
    },
    {
      "name": "code_analyzer",
      "arguments": {
        "dir_path": "src",
        "include_tree": true,
        "include_content": false
      }
    }
  ]
}
```

### Task Management and File Operations

```json
{
  "invocations": [
    {
      "name": "tasklist",
      "arguments": {
        "title": "Project Setup",
        "tasks": [
          {"title": "Analyze requirements", "status": "running"},
          {"title": "Create project structure", "status": "ready"},
          {"title": "Implement core features", "status": "ready"}
        ]
      }
    },
    {
      "name": "read_file",
      "arguments": {
        "file_path": "package.json"
      }
    },
    {
      "name": "grep",
      "arguments": {
        "pattern": "import",
        "glob": "src/**/*.js"
      }
    }
  ]
}
```

## Common Mistakes to Avoid

❌ **Don't** serialize the arguments as strings:
```json
{
  "invocations": [
    {
      "name": "read_file",
      "arguments": "{\"file_path\": \"README.md\"}"  // WRONG!
    }
  ]
}
```

✅ **Do** provide arguments as direct objects:
```json
{
  "invocations": [
    {
      "name": "read_file",
      "arguments": {
        "file_path": "README.md"  // CORRECT!
      }
    }
  ]
}
```

## Benefits of Using Batch Tool

1. **Reduced Latency**: Execute multiple operations in a single API call

2. **Better User Experience**: Fewer back-and-forth interactions mean faster responses

3. **Coordinated Operations**: Perform multiple related operations together

4. **Efficient Information Gathering**: Combine multiple data sources in one call

## When to Use Batch Tool

Use the batch tool when:

- You need information from multiple sources at once
- You're performing several file operations that could run in parallel
- You want to combine thinking and tasklist operations with other tools
- You need to update multiple aspects of a system simultaneously
- You're creating a complex workflow that involves multiple tools

## When Not to Use Batch Tool

Avoid using batch tool when:

- You only need to call a single tool
- Operations must be performed sequentially with dependencies
- You need to check the result of one operation before deciding on the next