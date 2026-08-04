# Google Drive Model Context Protocol (MCP) Server

An Model Context Protocol (MCP) server written in Python that enables AI assistants (such as Claude Desktop or Cursor) to search Google Drive, inspect metadata, filter PDFs, and read document contents via standard JSON-RPC tools.

<img src="../assets/MCP%20Inspector.png" alt="MCP Inspector UI showing Google Drive Server tools" width="950">

---

## Features (Version 2.0.0)

- **`search_files`**: Search files in your Google Drive by name or keyword with configurable result limits.
- **`list_recent_files`**: Fetch the most recently modified files across your Drive.
- **`list_pdfs`**: Filter and list all PDF documents sorted by last modified date.
- **`search_pdfs`**: Search specifically for PDF documents matching a query string.
- **`get_file_metadata`**: Retrieve detailed file information (size, owner email, creation date, direct web links).
- **`read_google_doc`**: Read plain-text contents of Google Docs directly using their file IDs.
- **OAuth 2.0 Integration**: Safe read-only authentication workflow with persistent local tokens (`token.json`) and silent automatic token refresh.

---

## Directory Structure

```text
MCP Google Drive/
├── server.py             # Main MCP server script (v2.0.0)
├── requirements.txt      # Python dependencies
├── credentials.json      # Google Cloud OAuth client credentials (user-supplied)
├── token.json            # Generated OAuth access tokens (auto-created on first run)
└── README.md             # Project documentation
