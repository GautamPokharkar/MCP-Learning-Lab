from __future__ import annotations

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from mcp.server.fastmcp import FastMCP  

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

mcp = FastMCP("Google Drive")


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
def list_recent_files(limit: int = 10) -> str:
    """List the most recently modified files in Google Drive."""
    try:
        service = get_drive_service()
        results = service.files().list(
            q="trashed = false",
            orderBy="modifiedTime desc",
            pageSize=limit,
            fields="files(id, name, mimeType, modifiedTime)",
            corpora="user",
        ).execute()

        files = results.get("files", [])
        if not files:
            return "No recent files found."

        return "\n".join(
            f"{item['name']} | {item['id']} | {item.get('mimeType', '')} | {item.get('modifiedTime', '')}"
            for item in files
        )
    except HttpError as e:
        return f"Drive API error: {e}"


@mcp.tool()
def list_pdfs(limit: int = 10) -> str:
    """List all PDF files stored in Google Drive."""
    try:
        service = get_drive_service()
        results = service.files().list(
            q="mimeType = 'application/pdf' and trashed = false",
            orderBy="modifiedTime desc",
            pageSize=limit,
            fields="files(id, name, mimeType, modifiedTime)",
            corpora="user",
        ).execute()

        files = results.get("files", [])
        if not files:
            return "No PDF files found."

        return "\n".join(
            f"{item['name']} | {item['id']} | {item.get('modifiedTime', '')}"
            for item in files
        )
    except HttpError as e:
        return f"Drive API error: {e}"


@mcp.tool()
def search_pdfs(query: str, limit: int = 5) -> str:
    """Search for PDF files by name or keyword."""
    try:
        service = get_drive_service()
        safe_query = query.replace("'", "\\'")
        results = service.files().list(
            q=f"mimeType = 'application/pdf' and name contains '{safe_query}' and trashed = false",
            pageSize=limit,
            fields="files(id, name, mimeType, modifiedTime)",
            corpora="user",
        ).execute()

        files = results.get("files", [])
        if not files:
            return "No matching PDF files found."

        return "\n".join(
            f"{item['name']} | {item['id']} | {item.get('modifiedTime', '')}"
            for item in files
        )
    except HttpError as e:
        return f"Drive API error: {e}"


@mcp.tool()
def get_file_metadata(file_id: str) -> str:
    """Get detailed metadata about a specific file (size, owners, timestamps, links)."""
    try:
        service = get_drive_service()
        fields = "id, name, mimeType, size, createdTime, modifiedTime, owners(displayName, emailAddress), webViewLink, shared"
        file = service.files().get(fileId=file_id, fields=fields).execute()

        owners = ", ".join([f"{o.get('displayName', '')} ({o.get('emailAddress', '')})" for o in file.get("owners", [])])
        size_bytes = file.get("size", "N/A (Google Doc/Folder)")

        return (
            f"File Name: {file.get('name')}\n"
            f"ID: {file.get('id')}\n"
            f"Type: {file.get('mimeType')}\n"
            f"Size: {size_bytes} bytes\n"
            f"Created: {file.get('createdTime')}\n"
            f"Last Modified: {file.get('modifiedTime')}\n"
            f"Owners: {owners}\n"
            f"Shared: {file.get('shared', False)}\n"
            f"Web Link: {file.get('webViewLink')}"
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