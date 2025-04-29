# Project migrated to AMZN_AKI
# Check docs under https://code.amazon.com/packages/AMZN_AKI/blobs/mainline/--/docs/ for the latest version

# Setting Up Chat History in Aki

Aki supports persistent chat history, allowing conversations to be saved and resumed between sessions. This feature needs to be manually enabled.

## Enabling Chat History

1. **Edit your Aki environment file**:
Edit ~/.aki/.env

   ```bash
   AKI_CHAT_HISTORY_ENABLED=true
   ```

2. **Set database configuration**:

Edit ~/.aki/.env

   ```bash
   # SQLite configuration 
   AKI_DATA_SOURCE=sqlite

   # PostgreSQL configuration 
   AKI_DATA_SOURCE=postgres
   ```

## Chat History Features

When enabled, chat history provides:

- **Persistent conversations** across sessions
- **Resume previous chats** where you left off
- **Conversation management** in the sidebar
- **Search functionality** through past discussions

## Privacy & Security

- Chat history is stored locally on your machine
- Data is never sent to external servers
- You can delete history at any time

## Managing Chat History

- **View history**: Click on past conversations in the sidebar
- **Delete conversations**: Use the delete button next to conversation entries
- **Clear all history**: Delete the database file (`~/.aki/chat_history.db`)

## Troubleshooting

If you encounter issues with chat history:

1. **Verify configuration**:
   ```bash
   grep AKI_CHAT ~/.aki/.env
   ```

2. **Check database access**:
   ```bash
   # For SQLite
   ls -la ~/.aki/chat_history.db

   # For PostgreSQL
   psql -U $USER -d postgres -c "SELECT 1"
   ```

3. **Restart Aki** after making configuration changes

4. **Reset chat history** if corrupted:
   ```bash
   rm ~/.aki/chat_history.db
   ```