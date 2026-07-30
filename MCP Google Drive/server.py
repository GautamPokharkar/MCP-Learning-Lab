from __future__ import annotations

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from mcp.server import MCPServer

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

mcp = MCPServer("Google Drive")


def get_drive_service():
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    "Missing credentials.json. Download it from Google Cloud and place it next to server.py."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return build("drive", "v3", credentials=creds)


@mcp.tool()
def search_files(query: str, limit: int = 5) -> str:
    """Search Google Drive for files by name."""
    try:
        service = get_drive_service()
        safe_query = query.replace("'", "\\'")
        results = service.files().list(
            q=f"name contains '{safe_query}' and trashed = false",
            pageSize=limit,
            fields="files(id, name, mimeType, modifiedTime)",
            corpora="user",
        ).execute()

        files = results.get("files", [])
        if not files:
            return "No files found."

        return "\n".join(
            f"{item['name']} | {item['id']} | {item.get('mimeType', '')} | {item.get('modifiedTime', '')}"
            for item in files
        )
    except HttpError as e:
        return f"Drive API error: {e}"


@mcp.tool()
def read_google_doc(file_id: str) -> str:
    """Read a Google Docs document as plain text."""
    try:
        service = get_drive_service()
        meta = service.files().get(fileId=file_id, fields="name, mimeType").execute()

        if meta["mimeType"] != "application/vnd.google-apps.document":
            return f"Unsupported file type: {meta['mimeType']}. This tool only reads Google Docs."

        content = service.files().export(fileId=file_id, mimeType="text/plain").execute()
        text = content.decode("utf-8") if isinstance(content, (bytes, bytearray)) else str(content)
        return text[:12000]
    except HttpError as e:
        return f"Drive API error: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")