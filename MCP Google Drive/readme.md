
---

```markdown
# Google Drive Model Context Protocol (MCP) Server

An Model Context Protocol (MCP) server written in Python that enables AI assistants (such as Claude Desktop or Cursor) to search Google Drive and read document contents via standard JSON-RPC tools.

## Features

- **`search_files`**: Search files in your Google Drive by name or keyword with configurable result limits.
- **`read_google_doc`**: Read plain-text contents of Google Docs directly using their file IDs.
- **OAuth 2.0 Integration**: Safe authentication workflow with persistent local tokens (`token.json`).

---

## Directory Structure

```text
MCP/
├── server.py             # Main MCP server script
├── requirements.txt      # Python dependencies
├── credentials.json      # Google Cloud OAuth client credentials (user-supplied)
├── token.json            # Generated OAuth access tokens (auto-created on first run)
└── README.md             # Project documentation

```

---

## Prerequisites

* **Python 3.10+** installed.
* A **Google Cloud Console** project with the **Google Drive API** enabled.
* Downloaded OAuth 2.0 Desktop credentials saved as `credentials.json` in the root folder.

---

## Quickstart Setup

### 1. Clone & Set Up Environment

```bash
# Create and activate virtual environment
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On macOS/Linux:
source venv/bin/activate

```

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt

```

### 3. Add Google OAuth Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Drive API**.
3. Configure the **OAuth Consent Screen** (set application type to *External* and add your email under **Test Users**).
4. Create **OAuth Client ID** credentials with application type **Desktop App**.
5. Download the credentials JSON, rename it to `credentials.json`, and place it in the project root directory.

---

## Development & Testing

You can test and inspect the server using the official **MCP Inspector**:

```bash
mcp dev server.py

```

1. The MCP Inspector UI will launch in your browser (typically at `http://localhost:5173`).
2. On your first tool execution, a browser tab will automatically open for Google OAuth authorization.
3. Once authorized, `token.json` will be saved locally, and tool execution will run seamlessly.

---

## Available Tools

### `search_files`

* **Description**: Searches Google Drive for matching filenames.
* **Parameters**:
* `query` (string, required): Search keyword or filename fragment.
* `limit` (integer, optional): Maximum number of results to return (default: `5`).



### `read_google_doc`

* **Description**: Retrieves text content from a specified Google Doc.
* **Parameters**:
* `file_id` (string, required): The Google Drive File ID.



---

## License

MIT License

```

```
