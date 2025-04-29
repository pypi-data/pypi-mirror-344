# Project migrated to AMZN_AKI
# Check docs under https://code.amazon.com/packages/AMZN_AKI/blobs/mainline/--/docs/ for the latest version

# Aki Export Feature

Aki provides a powerful conversation export feature that allows users to save their chat sessions in various formats for reference, sharing, or analysis.

## Basic Export Usage

To export your conversation:

1. Type `/Export` in the chat input
2. Choose from the available format options:
   - JSON: Structured data format (best for programmatic or debugging use)
   - Markdown: Formatted document (best for reading/sharing)
3. Click on your preferred format to download the file

## Direct Format Export

For power users who know which format they want, Aki supports direct format specification:

### Syntax

```
/Export <format>
```

Where `<format>` can be:

| Short Format | Long Format | Description |
|--------------|-------------|-------------|
| j            | json        | JSON export |
| m            | markdown    | Markdown export |

### Examples

```
/Export j
```
Directly exports the conversation as JSON without showing the format selection UI.

```
/Export markdown
```
Directly exports the conversation as Markdown.

## Export Content

JSON exported file contains:

- Conversation thread ID
- Chat profile used
- Message history with:
  - User messages
  - Assistant responses
  - Tool executions (when applicable)
  - Timestamps
- Limitations: some old messages might not be shown if triggers conversation summarization

Markdown exported file contains:
- All conversations between Assistant and User
- No tool messages

## Technical Details

The export functionality maintains message attribution and structure across formats:

- **JSON**: Full structured data including message types and metadata
- **Markdown**: Formatted with headers for each speaker and code blocks for tool messages
- **Plain text**: Simple format with speaker labels

## Privacy Note

Exported conversations are saved locally to your device. No data is sent to external servers during the export process.