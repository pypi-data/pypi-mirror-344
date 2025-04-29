# Project migrated to AMZN_AKI
# Check docs under https://code.amazon.com/packages/AMZN_AKI/blobs/mainline/--/docs/ for the latest version

# GrepTool - Fast Content Searching

## Overview

GrepTool is a powerful content search tool that leverages ripgrep (or falls back to standard grep) to efficiently search codebase contents using regular expressions. It's designed for performance, even in large codebases, and provides rich output including line numbers, matching content, and file metadata.

## Features

- **Regular Expression Search**: Search file contents using powerful regex patterns
- **Fast Performance**: Uses ripgrep (when available) for extremely fast searches
- **File Filtering**: Include only specific file types (.py, .js, etc.)
- **Sort Options**: Sort results by modification time, path, or relevance
- **Rich Results**: Get line numbers, content snippets, and file metadata
- **Fallback Mechanism**: Uses standard grep if ripgrep isn't available

## Usage Examples

### Find TODO Comments in Python Files

```python
from amzn_aki.tools.file_management.grep_tool import GrepTool

grep = GrepTool()
results = grep.run(
    pattern="TODO",
    path="src",
    glob="*.py",
    sort_by="modified"
)

# Parse JSON results
import json
todos = json.loads(results)

# Process matches
for match in todos["matches"]:
    print(f"{match['path']}:{match['line_number']}: {match['content']}")
```

### Find Error Patterns in Log Files

```python
grep = GrepTool()
results_json = grep.run(
    pattern="Error|Exception|Failed",
    path="logs",
    glob="*.log",
    case_sensitive=False
)

results = json.loads(results_json)
print(f"Found {results['total_matches']} errors in logs")
```

### Search for Function Definitions

```python
grep = GrepTool()
results_json = grep.run(
    pattern="function\\s+\\w+",  # Match "function" followed by whitespace and word chars
    path="src",
    glob="*.js"
)

results = json.loads(results_json)
for match in results["matches"]:
    print(f"Found function in {match['path']} at line {match['line_number']}")
```

## Parameters

- **pattern** (required): The regular expression pattern to search for
- **path** (default=`".")`): Directory to search in
- **glob** (default=`""`): Glob pattern for filtering files (e.g., `*.py`, `*.{ts,tsx}`, `src/**/*.js`)
- **max_results** (default=`50`): Maximum number of results to return
- **case_sensitive** (default=`False`): Whether to perform case-sensitive matching
- **sort_by** (default=`"modified"`): How to sort results: `modified` (most recent first), `path` (alphabetically), or `relevance`

## Result Format

The tool returns a JSON string containing:

```json
{
  "pattern": "search pattern",
  "path": "search path",
  "resolved_path": "absolute path",
  "glob": "file pattern",
  "case_sensitive": false,
  "matches": [
    {
      "path": "file/path.py",
      "line_number": 42,
      "content": "matching line content",
      "modified_time": "2023-05-15 10:30:45"
    },
    // More matches...
  ],
  "total_matches": 5,
  "search_method": "ripgrep",
  "error": null
}
```

## Performance Considerations

- For best performance, install ripgrep (`rg`) on your system
- Results are sorted by modification time by default, which requires filesystem access
- Consider limiting results with `max_results` for very large codebases
- Complex regex patterns may be slower, so use simpler patterns when possible